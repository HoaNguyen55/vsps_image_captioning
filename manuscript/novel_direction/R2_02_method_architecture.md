# R2-02. Kiến trúc phương pháp Know-and-Mention (KaM): một mô hình, không phải một dây chuyền

*Vai trò: METHOD ARCHITECT. Vòng 2, 11/10/2026. Mở rộng `05_TONG_HOP_XEP_HANG.md` và các hướng A+B của `04_alternatives.md`, không làm lại. Mọi con số thời gian GPU là **ước lượng, chưa đo**.*

**Tóm tắt 5 dòng**
1. Năm tham chiếu KTVIC được mô hình hóa là năm lần "quyết định nhắc" độc lập trên một đối tượng có thật: k ~ 1[e=1]·BetaBin(5, μ). Đây là bài toán PU learning với propensity phụ thuộc đối tượng (SAR), và **propensity chính là mentionability**.
2. Năm người gán làm μ **nhận dạng được chỉ từ các đối tượng đã được nhắc** (phân phối k cắt cụt tại 0). Từ đó có P(e=1) = P(k≥1)/ψ(μ), ở dạng đóng. Cũng từ đó thấy rõ: với đối tượng ít nổi bật, tham chiếu không mang thông tin về sự tồn tại, nên *bắt buộc* phải dùng niềm tin nội tại của mô hình.
3. Luật quyết định Bayes cho F1 kiểu KTVIC (P micro, R macro) là một ngưỡng riêng cho từng ảnh trên r = π·ψ, cộng một sàn trung thực π ≥ τ_e. Faithfulness và độ khớp tham chiếu nhờ đó do hai biến khác nhau điều khiển.
4. Captioner học **hành động Bayes trên chính caption mô hình tự sinh**, không học template: (i) một probe "neo" trên trạng thái thị giác, với các tầng dưới ℓ* được đóng băng; (ii) chọn mẫu tự sinh theo tiện ích U; (iii) token điểm vận hành. Kết quả là một lượt forward duy nhất cho mỗi điểm trên đường P/R.
5. Những phần mới: cách đọc 5 người gán như propensity của PU, phép phân rã r = π·ψ cùng ngưỡng đóng, nguyên lý "chỉ dạy điều mô hình biết" (Gekhman) chuyển sang thị giác, và neo niềm tin chống tự lừa. Mọi phần còn lại là công cụ chuẩn, được ghi rõ ở §10.

---

## 1. Mô hình xác suất: hai biến ẩn cho mỗi đối tượng

**Đơn vị.** Một cặp (ảnh i, lớp đối tượng c) trong lexicon 113 mục. Đây đúng là đơn vị mà `scripts/object_prf.py` dùng để chấm: tập lớp duy nhất trên mỗi ảnh, gold là hợp các lớp của 5 tham chiếu.

**Tập ứng viên.** C_i = các đề xuất của Qwen ở Stage 1 (`generate.py`), hợp với mọi lớp mà tham chiếu nhắc. Dữ liệu train có 13.031 đối tượng gold kèm số lần nhắc k.

Với mỗi o ∈ C_i có:
- **e_o ∈ {0,1}: tồn tại.**
- **μ_o ∈ [0,1]: mentionability.** Đây là xác suất một người Việt *nhắc* o khi mô tả ảnh, *với điều kiện o có thật*.
- **k_o ∈ {0..5}: số người gán đã nhắc.** Đây là biến quan sát.

Mô hình sinh, với z_o là bằng chứng tồn tại (§3) và x_o là đặc trưng nổi bật (§4):

$$
e_o \sim \mathrm{Bern}(\pi(z_o, x_o)),\qquad
\mu_o \sim \mathrm{Beta}(a(x_o), b(x_o)),\qquad
k_o \mid e_o,\mu_o \sim \begin{cases}\mathrm{Bin}(5,\mu_o) & e_o=1\\ \delta_0 & e_o=0\end{cases}
$$

Biến μ được rút từ phân phối Beta để mô hình hóa việc các người gán *tương quan* với nhau. Số liệu đo được rất phân tán: 4.967 đối tượng có k=1 và 1.550 có k=5, điều mà một Binomial với μ chung không thể sinh ra.

Ký hiệu xác suất một đối tượng có thật lọt vào gold:

$$
\psi(x) \;=\; P(k\ge1\mid e=1,x) \;=\; 1-\frac{B(a,\,b+5)}{B(a,b)} .
$$

**Mệnh đề 1 (nhận dạng được).**
(a) Phân phối cắt cụt P(k | k≥1, x) = BetaBin(k; 5, a, b) / ψ(x) chỉ phụ thuộc (a, b). Vì vậy μ ước lượng được **chỉ từ các đối tượng đã được nhắc**, không cần nhãn tồn tại.
(b) Sau đó π(z, x) = P(k≥1 | z, x) / ψ(x).
(c) Posterior tồn tại của một đối tượng không ai nhắc là

$$
q_o \;=\; P(e_o=1\mid k_o=0) \;=\; \frac{\pi\,(1-\psi)}{\pi\,(1-\psi) + (1-\pi)} .
$$

*Hệ quả.* Khi ψ → 0, tức đối tượng rất ít nổi bật, thì q → π. Tham chiếu khi đó **không chứa thông tin** về việc đối tượng có tồn tại hay không, và π phải lấy từ bằng chứng thị giác z. Đây là lý do hình thức, không phải lý do kỹ thuật, khiến trục "biết" là bắt buộc. Nó cũng giải thích vì sao gold dựa trên tham chiếu phạt oan đúng nhóm 38% đối tượng chỉ 1/5 người nhắc.

**Định vị.**
- Dawid & Skene (1979) mô hình người gán *sai* nhãn. Ở đây người gán không sai mà *chọn không nói*. Đó là cơ chế bị che kiểu SAR của PU learning (Bekker et al., ECML-PKDD 2019; Bekker & Davis, Machine Learning 2020).
- Lý thuyết SAR-PU cần giả định để nhận dạng propensity. Có 5 lần gán độc lập *đã đủ* để nhận dạng nó. Theo hiểu biết của tôi, chưa ai dùng nhận xét này cho captioning (**UNVERIFIED** về tính mới tuyệt đối; cần một lần tìm kiếm có mục tiêu).

## 2. Caption nên tối đa hóa cái gì: luật quyết định

Xác suất một đối tượng được mention là đúng so với tham chiếu là r_o = P(k_o ≥ 1) = π_o·ψ_o. Metric gồm P micro trên toàn corpus và R macro theo ảnh (`object_prf.py`).

Gọi M̄ là số mention trung bình mỗi ảnh và g_i = E|G_i| = Σ_{o∈C_i} r_o + ĝ_0. Ở đây ĝ_0 là khối gold kỳ vọng nằm ngoài tập đề xuất; trên train nó khoảng 30%, suy từ bảng recall đề xuất 62–73.

Tuyến tính hóa F = 2PR/(P+R) quanh điểm tối ưu và thêm o vào ảnh i:
- ΔP ≈ (r_o − P)/(N·M̄)
- ΔR ≈ r_o/(N·g_i)

Thêm o có lợi khi R²·ΔP + P²·ΔR > 0, tức là

$$
\boxed{\; r_o \;>\; t_i \;=\; \frac{P^\ast}{1+(P^\ast/R^\ast)^2\,\bar M/g_i}\;}
\qquad\text{và}\qquad \boxed{\;\pi_o \ge \tau_e\;}
$$

Kiểm tra lại: khi P = R = F và M̄ = g_i thì t = F/2. Đây đúng là kết quả của Lipton et al. (ECML-PKDD 2014), nên bản mở rộng sang P micro, R macro là nhất quán. Ngưỡng t_i *tự thích nghi*: ảnh có ít gold thì g_i nhỏ, mỗi đối tượng đáng giá recall hơn, nên ngưỡng thấp hơn. (P\*, R\*) giải bằng lặp điểm bất động trên dev, hội tụ sau vài vòng.

**Sàn trung thực π ≥ τ_e** là ràng buộc thứ hai và độc lập: tỉ lệ ảo giác kỳ vọng so với *thực tại* (không phải so với tham chiếu) là Σ(1−π)/|M| ≤ ε. Hai trục giờ tách hẳn:
- đối tượng có thật nhưng ψ thấp thì bị loại bởi t_i, mà faithfulness không mất gì;
- đối tượng nổi bật có π = 0,8 thì được giữ, kể cả khi Vintern trả lời UNCERTAIN.

Sự đánh đổi chỉ còn lại ở nhóm π ∈ [t, τ_e), và nhóm này *đếm được*. Tùy chọn mở rộng là cho nhóm này đi qua kênh hedge của hướng C.

**Mục tiêu khi train** dùng thêm k quan sát được, theo kiểu empirical-Bayes. Trên ảnh train:

$$
r^{\text{train}}_o = \tilde\pi_o\,\psi(\tilde a_o,\tilde b_o),\quad \tilde a=a+k,\; \tilde b=b+5-k,\quad \tilde\pi_o=\begin{cases}1 & k\ge1\\ q_o & k=0\end{cases}
$$

Sàn π_o ≥ τ_e **vẫn dùng π từ bằng chứng thị giác**, kể cả khi k ≥ 1. Đối tượng mà người nhắc nhưng mô hình không "biết" (π thấp) bị loại khỏi target. Đây là phiên bản thị giác của Gekhman et al. (EMNLP 2024): SFT trên kiến thức mô hình không có sẽ dạy mô hình bịa. Baseline phản chứng trực tiếp đã có sẵn là `scripts/build_gold_sft.py`, tức SFT thẳng trên tham chiếu.

## 3. Ước lượng e từ trạng thái nội tại của chính captioner

**Probe không truy vấn (query-free MIL probe).** Trong template chat của Qwen2.5-VL, các token thị giác đứng **trước** mọi chữ của người dùng. Dưới causal attention, hidden state của chúng ở mọi tầng LM chỉ phụ thuộc vào ảnh và system prompt cố định. Không có tên đối tượng nào rò vào được. Với h_t^ℓ ∈ ℝ^3584 tại token t và tầng ℓ:

$$
s_c(I) = \tau\log\sum_{t} \exp\!\big((W h^{\ell}_t)^\top u_c/\tau\big),
\qquad u_c=\text{embedding (đóng băng) của danh từ đầu kèm loại từ}
$$

- Probe là song tuyến (bilinear), nên chia sẻ được giữa 113 lớp và tổng quát được sang lớp hiếm.
- Pooling dùng LSE (soft-max kiểu multiple-instance), nghĩa là "có một patch nào đó là c".
- Tầng được quét trên ℓ ∈ {7, 14, 21, 28}, chọn bằng dev log-likelihood của mô hình §1, **không** chọn theo đồng thuận với Vintern.

**Nhãn không cần gold người: PU-EM có trọng số propensity.**
- Dương là mọi đối tượng có k ≥ 1. Chúng chắc chắn có thật vì có người thật nhắc.
- Không nhãn là đề xuất có k = 0, cộng với các lớp vắng được lấy mẫu theo PMI đồng xuất hiện cao. Đây là âm tính khó, ví dụ "đĩa" trong cảnh bàn ăn.
- E-step tính q_o (§1c). M-step huấn luyện s với trọng số dương 1/ψ_o (IPW, như SAR-EM) và trọng số âm (1 − q_o).

Nếu không có IPW, probe sẽ học **độ nổi bật thay cho sự tồn tại**, vì các dương tính bị chọn lệch về đối tượng lớn và ở trung tâm. Ablation A5 đo đúng điều này.

**Gộp với Vintern.** Đặt π(z, x) = σ(β₁s_c + β₂ℓ_V + β₃·1[UNC] + β₄·1[REJ] + γᵀx_e). Ở đây ℓ_V là logit có/không từ chế độ logit verifier (gate T0.5, κ = 0,79 so với K=5) và x_e là vài đặc trưng hình học (diện tích, độ nét từ `verify.py`). Vintern trở thành **một cảm biến trong π**, không còn là trọng tài có quyền phủ quyết. Các hệ số β cho biết nó thực sự đóng góp bao nhiêu.

**Đối chứng rò tiên nghiệm** (đều là cổng dừng, ngưỡng đăng ký trước):

| # | Đối chứng | Đạt nếu |
|---|---|---|
| L1 | Inpainting phản thực: 100 ảnh xóa một đối tượng đồng xuất hiện mạnh (LaMa, WACV 2022) | s_c giảm, AUROC(trước vs sau) ≥ 0,85 |
| L2 | Pointing game: argmax_t nằm trong box của đối tượng | ≫ tỉ lệ diện tích box (cơ hội) |
| L3 | Baseline "gist": probe trên trung bình toàn cục, và baseline đồng xuất hiện (logistic từ các lớp khác) | MIL probe hơn ≥ 0,05 AUROC trong từng cụm cảnh |
| L4 | Probe trên token truy vấn "Trong ảnh có X không?" | Phải *kém hơn* hoặc lệch tiên nghiệm hơn query-free trên L1 |

## 4. Học μ từ 5 người gán của KTVIC

**Mô hình.** Beta-binomial hồi quy: mean m(x) = σ(gᵀx), độ phân tán φ theo nhóm loại từ. Fit bằng MLE trên phân phối k *cắt cụt* (Mệnh đề 1a), trên CPU, mất vài phút.

**Đặc trưng x** (chỉ những thứ có được từ ảnh và đề xuất; box cho đối tượng chưa được đề xuất lấy bằng một lượt grounding của Qwen):
- *Hình học:* diện tích, độ trung tâm, số thể hiện, mức che khuất, độ nét.
- *Tiên nghiệm lớp:* tỉ lệ nhắc của lớp trên train (dùng leave-image-out để tránh rò).
- *Đồ thị:* bậc của đối tượng trong đồ thị quan hệ Stage 1. Đối tượng bị người *cưỡi, cầm, bán* thì dễ được nhắc hơn.
- *Đặc trưng tiếng Việt:*
  - **loại từ** ∈ {người, con, chiếc, cái, quả, tấm…}. Loại từ mã hóa độ hữu sinh và hình dạng. "cái" là loại từ mặc định, thường gặp ở vật nền.
  - **vai khung cảnh:** danh từ làm bổ ngữ địa điểm như "trên *đường*", "ở *chợ*", "bên *sông*". Nhóm này được nhắc thường xuyên dù chiếm ít pixel.
  - **tỉ lệ nhắc-đầu-câu** của lớp. Tiếng Việt là ngôn ngữ thiên chủ đề, nên NP đầu tiên gần như luôn là chủ thể chính.

**Đa nhiệm: thứ tự nhắc đầu tiên.** Từ 5 tham chiếu có hạng nhắc đầu tiên ρ_o. Mô hình học kèm một đầu ra thứ tự (ordinal) ρ̂(x), dùng ở §6 để sắp thứ tự nội dung. ρ là nhãn, không phải đặc trưng tại test.

**Kiểm định không cần gold (leave-one-annotator-out).** Fit trên 4 người, dự đoán người thứ 5 nhắc gì trong các đối tượng có k₄ ≥ 1. Báo cáo AUROC và ECE. Kiểm tra posterior-predictive histogram k so với phân phối quan sát 4.967 / 3.229 / 2.026 / 1.259 / 1.550. Đây là H-A2 (`04_alternatives.md`) trong dạng chặt hơn.

## 5. Huấn luyện captioner: một lượt forward tại điểm vận hành tối ưu

Có bốn lựa chọn: (a) token kế hoạch tường minh; (b) đầu mention chặn decoding; (c) tự chưng cất kiểu EM; (d) RL. Chọn **(c) làm lõi, (b) làm biến thể suy luận, bỏ (d)**. Lý do: RL on-policy với 7B 4-bit trên một chiếc 3090 quá chậm. Còn (a) làm caption dài thêm và lẫn với lỗi realisation. Thiết kế cụ thể:

1. **Neo niềm tin (belief anchor).** LoRA chỉ gắn vào các tầng *trên* ℓ\*. Không gọi `enable_input_require_grads`, nên backward dừng ở ℓ\*. Vì thế input của probe giống hệt mô hình gốc trong suốt quá trình train, và captioner **không thể học cách đánh lừa chính probe của nó** (lỗi tự xác nhận). Đây là lựa chọn kiến trúc, không phải mẹo. Đi kèm là một khoản tiết kiệm compute ước lượng 25–35% so với LoRA toàn tầng như `train_stage2.py` hiện làm.
2. **Target là caption tự sinh** của mô hình (§6), được chọn theo tiện ích:
$$
U(y)=\mathrm{F1}\big(M(y),S^\ast_i\big)\;+\;\lambda_C\,\mathrm{CIDEr\text{-}D}(y;\mathrm{refs}_i)\;-\;\lambda_H\!\!\sum_{o\in M(y)}\!\!(1-\pi_o)\;-\;\lambda_\rho\,(1-\tau_K(M(y),\hat\rho))
$$
Ở đây M(y) là các lớp lexicon có trong y, S\*_i là kế hoạch Bayes (§2), và τ_K là Kendall tau giữa thứ tự nhắc trong y và thứ tự dự đoán ρ̂.
3. **Token điểm vận hành.** Mỗi ảnh train được gán ngẫu nhiên một mức ω ∈ {P, F, R}, ứng với (τ_e, hệ số nhân t_i) ∈ {(0,9; 1,3), (0,8; 1,0), (0,6; 0,7)}, và tiền tố `<ω>` được thêm vào prompt. Dữ liệu không tăng lên. Tại test, mỗi ω là một lượt forward, nên **một mô hình vẽ được cả đường P/R**. Như vậy kiểm định được tính trội Pareto so với zero-shot và VSPS ở từng điểm, đúng yêu cầu của critique O7 về khoảng hụt khi chưng cất.
4. **Biến thể MGD (mention-gated decoding), không bắt buộc.** Hai đầu e và μ được chưng cất vào mô hình (MIL trên token thị giác) và chạy *trong prefill*, tức gần như miễn phí. Khi decode đến danh từ đầu sau loại từ thuộc lớp c, cộng thêm vào logit một lượng β·(logit r̂_c − logit t). Biến thể này vẫn là một lượt.
5. **Tùy chọn DPO** (hạ tầng sẵn có trong `train_stage2.py`): cặp (mẫu U cao nhất, mẫu U thấp nhất) của cùng ảnh. Đây chỉ là thí nghiệm phụ.

**Algorithm 1: KaM**
```
Input : train images I with 5 refs, Stage-1 candidates C_i, Vintern logits ℓ_V
Output: LoRA adapter θ (layers > ℓ*), heads (W, g)

# --- (A) latent model: once, base model frozen ---
H ← prefill_vision_states(Qwen_base, I, layers={7,14,21,28})     # no text query
fit (a,b) by truncated-BetaBin MLE on {o : k_o ≥ 1}               # Prop. 1a
init s via IPW-PU (positives k≥1, weight 1/ψ)
repeat until Δloglik < 1e-3:                                       # PU-EM
    q_o ← π(1-ψ)/(π(1-ψ)+1-π)        for k_o = 0                  # E-step
    fit W (probe), β (fusion) on soft labels {1 | k≥1} ∪ {q_o | k=0}   # M-step
choose ℓ* by dev loglik;  run leakage gates L1–L4 → STOP if failed

# --- (B) self-distillation, rounds t = 0..T-1 (T=2) ---
π_0 ← Qwen_base
for t in 0..T-1:
    for each image i, ω ~ Unif{P,F,R}:
        S*_i ← {o : r^train_o > m_ω·t_i  and  π_o ≥ τ_e(ω)}       # §2, rule
        Y ← sample K=6 captions from π_t(<ω>, I_i)
        if max_y F1(M(y),S*_i) < 0.8:                             # plan not reached
            Y ← Y ∪ sample K from Qwen_base(plan-prompt(S*_i in ρ̂ order))
        Y ← {y ∈ Y : M(y) ∖ S*_i contains no o with π_o < τ_e}    # grounding filter
        D_t ← D_t ∪ {(<ω>, I_i, argmax_y U(y))}
    θ ← QLoRA-SFT(layers > ℓ*, D_t);  π_{t+1} ← Qwen_base ⊕ θ
    report: target-vs-student P/R gap, distinct-n, KL(π_{t+1} ∥ base)
```
EM ở đây là EM thật trên (e, μ) ở phần (A). Phần (B) là self-training. Hai vòng được tách sạch, và chính nhờ belief anchor mà (A) không phải chạy lại sau mỗi vòng (B).

## 6. Vì sao CIDEr và BLEU tăng, không chỉ object F1

1. **Thay template bằng lời của chính mô hình.** Renderer hiện tại (`realize.py`) làm mất khoảng 7 điểm recall, sinh ra những câu như "Cái mũ này đang đạp xe", và có fluency người chấm là 3,17. Target của KaM là văn bản Qwen tự sinh, đã được lọc. Captioner vì thế học phân phối của *chính nó*. Giả thuyết là khoảng hụt target→student nhỏ hơn mức trượt 40,6 → 38,1 của v2, và bigram/4-gram tự nhiên hơn. Các `fix_classifiers`, `fix_adjective_order`, `fix_gendered_pronouns` của `realize.py` được giữ làm bộ lọc dữ liệu, không làm renderer.
2. **Đồng thuận.** CIDEr-D đặt trọng số tf-idf cho các n-gram mà nhiều tham chiếu cùng có. Chọn đối tượng theo ψ cao đồng nghĩa với chọn nội dung đồng thuận. Đây là cùng một biến, nên lợi ích về object và về CIDEr cùng hướng thay vì đánh đổi nhau.
3. **Thứ tự và độ dài.** Số hạng τ_K buộc caption mở đầu bằng chủ thể mà người Việt mở đầu, nên khớp được n-gram đầu câu. Kế hoạch S\* có kích thước gần với độ dài tham chiếu, tránh hình phạt độ dài Gaussian của CIDEr-D. Zero-shot dài 117 từ là ví dụ của mức phạt đó.
4. Thuộc tính và quan hệ: một mệnh đề SUPPORTED được đưa vào prompt kế hoạch khi và chỉ khi thực thể đầu của nó ∈ S\*, tức là kế thừa mentionability từ thực thể. Đây là chỗ đơn giản hóa có chủ ý. Cần mở rộng khi ablation cho thấy recall quan hệ bị giới hạn.

## 7. Ablation tách từng thành phần (3 seed, bootstrap cặp theo ảnh)

| ID | Thay đổi so với KaM đầy đủ | Cô lập điều gì |
|---|---|---|
| B0 | VSPS (Vintern SUPPORTED + template) | baseline |
| B1 | SFT thẳng trên tham chiếu (`build_gold_sft.py`) | "dạy điều không biết" (Gekhman) |
| B2 | Chọn mẫu tự sinh chỉ theo CIDEr (giống SCST) | KaM có phải chỉ là reward selection không |
| A1 | B0 nhưng e từ π (probe + Vintern), giữ template | trục tồn tại |
| A2 | A1 + ngưỡng r = πψ, giữ template | trục mentionability |
| A3 | Lựa chọn của VSPS + target tự sinh | chỉ phần rendering → CIDEr/BLEU |
| A4 | π chỉ dùng probe, hoặc chỉ dùng Vintern | giá trị của từng cảm biến |
| A5 | PU không có IPW | rò độ nổi bật vào e |
| A6 | μ từ nhãn nhị phân k ≥ 1 thay vì đếm k | giá trị của 5 người gán (Mệnh đề 1) |
| A7 | τ_e = 0 (bỏ sàn trung thực) | ảo giác trên gold-300 |
| A8 | probe trên token truy vấn | rò tiên nghiệm ngôn ngữ |
| A9 | LoRA toàn tầng, probe fit lại mỗi vòng | belief anchor |
| A10 | ngưỡng toàn cục so với t_i theo ảnh | ngưỡng thích nghi |
| A11 | T = 1 so với T = 2; K = 3 so với K = 6 | self-training |
| A12 | bật/tắt MGD; một token ω so với 3 mô hình riêng | suy luận |

Metric gồm hai cột: tham chiếu (P/R/F1, CIDEr-D, BLEU-4, ROUGE-L) và **gold-300 đầy đủ** (CHAIR-vi kiểu thực tại, ECE của π). Cùng với đó là đánh giá người về fluency và faithfulness trên 100 caption mỗi hệ.

## 8. Failure mode và cách phát hiện

| Lỗi | Dấu hiệu, cách phát hiện | Phản ứng |
|---|---|---|
| Probe học tiên nghiệm cảnh | L1–L3 trượt; AUROC trong cụm cảnh ≪ AUROC tổng | Dừng trục "biết"; chỉ báo cáo phép phân rã |
| Propensity sai dạng, người gán phụ thuộc nhau | Posterior-predictive histogram k lệch; ECE leave-one-annotator-out > 0,1 | Thêm hỗn hợp Beta, hoặc φ theo lớp |
| ψ → 0 nên π/ψ bùng nổ | q dao động mạnh theo khởi tạo; phương sai bootstrap lớn | Kẹp ψ ≥ 0,05; báo cáo tỉ lệ đối tượng bị kẹp |
| Self-training trôi hoặc sụp mode | distinct-2 giảm, độ dài trôi, KL tăng, verbalization gap không giảm | Dừng ở T = 1; trộn 20% mẫu vòng 0 |
| Khoảng hụt khi chưng cất (O7) | P của target − P của student > 2 điểm trên dev | Chuyển sang ω = P; tăng λ_H |
| Bị buộc tội "tối ưu theo metric" | P tham chiếu tăng nhưng P gold-300 giảm | Đây là phát hiện cần báo cáo; τ_e là tham số kiểm soát |
| Lỗi ánh xạ lexicon | Audit 200 mention, F1 trích xuất < 0,9 | Sửa lexicon trước khi train |
| Caption theo kế hoạch bỏ sót mục | Coverage < 0,8 sau resample | Loại ảnh đó khỏi D_t, đếm và báo cáo |

## 9. Ước tính compute trên một RTX 3090 (ước lượng; phải đo 50 ảnh trước, theo O8)

| Bước | Ước lượng |
|---|---|
| Prefill 4-bit, 512 token thị giác, khoảng 4,8k ảnh; lưu 4 tầng chiếu ngẫu nhiên xuống 256 chiều (khoảng 1 MB/ảnh) | 0,5 GPU-h, khoảng 5 GB đĩa |
| Grounding box cho đối tượng có k ≥ 1 chưa được đề xuất | 1–2 GPU-h |
| PU-EM, μ-BetaBin, chọn ℓ\* | dưới 1 GPU-h + CPU |
| L1 inpainting (100 ảnh) + L2–L4 | khoảng 1 GPU-h |
| Lấy mẫu K = 6 × 3,7k ảnh (khoảng 80 token/caption) + resample theo kế hoạch | 5–9 GPU-h mỗi vòng |
| QLoRA SFT trên tầng > ℓ\* (so với khoảng nửa GPU-ngày hiện nay) | 8–12 GPU-h mỗi lần |
| KaM chính (T = 2) | khoảng 35 GPU-h |
| 12 ablation (A3–A12 chủ yếu tái dùng dữ liệu (B)) + 3 seed cho chính, B1 và A1 | khoảng 7–9 GPU-ngày |

Tổng cộng khoảng 2,5 tuần GPU, chạy song song với việc gán gold-300. Gold-300 chỉ cần cho cột thực tại và ECE, không chặn phần (A) hay (B).

## 10. Mới và chuẩn

| Thành phần | Trạng thái |
|---|---|
| Đọc 5 tham chiếu như propensity SAR-PU; mentionability = propensity; nhận dạng nhờ phân phối k cắt cụt (Mệnh đề 1) | **Mới** (khung PU và beta-binomial là chuẩn) |
| Phân rã r = π·ψ, cùng hệ quả "tham chiếu không mang thông tin tồn tại khi ψ → 0" | **Mới** |
| Ngưỡng đóng t_i cho P micro / R macro, cộng sàn π độc lập | Mở rộng nhỏ của Lipton 2014 / Nan 2012 |
| "Chỉ dạy điều mô hình biết" bằng probe nội tại, cho captioning | **Mới** cho VLM (ý tưởng gốc: Gekhman 2024, chữ) |
| Probe query-free trên token thị giác + belief anchor (LoRA trên ℓ\*) | **Mới** về cách dùng (probe là công cụ chuẩn) |
| Token điểm vận hành cho đường P/R của captioner | Mới vừa (control code là chuẩn: CTRL; Deng et al. 2020) |
| Đặc trưng mentionability tiếng Việt (loại từ, vai khung cảnh, thứ tự chủ đề) | Mới cho tiếng Việt (ý tưởng importance: Berg 2012) |
| IPW-PU-EM, rejection-sampling SFT, DPO, QLoRA, LaMa, CIDEr-D | Chuẩn |

**Tài liệu** (link chưa được tải lại trong vòng này; kiểm tra trước khi nộp):
- Dawid & Skene, *JRSS-C* 1979. doi:10.2307/2346806
- Elkan & Noto, *KDD* 2008. doi:10.1145/1401890.1401920
- Bekker, Robberechts & Davis, *ECML-PKDD* 2019. arXiv:1809.03207
- Bekker & Davis, *Machine Learning* 2020. arXiv:1811.04820
- Nan et al., *ICML* 2012. arXiv:1206.4625
- Lipton et al., *ECML-PKDD* 2014. arXiv:1402.1892
- Gekhman et al., *EMNLP* 2024. arXiv:2405.05904
- Berg et al., *CVPR* 2012. core.ac.uk/works/2253098
- Vedantam et al. (CIDEr), *CVPR* 2015. arXiv:1411.5726
- Rennie et al. (SCST), *CVPR* 2017. arXiv:1612.00563
- Zelikman et al. (STaR), *NeurIPS* 2022. arXiv:2203.14465
- Dong et al. (RAFT), *TMLR* 2023. arXiv:2304.06767
- Gulcehre et al. (ReST), arXiv:2308.08998, 2023 (preprint)
- Rafailov et al. (DPO), *NeurIPS* 2023. arXiv:2305.18290
- Dettmers et al. (QLoRA), *NeurIPS* 2023. arXiv:2305.14314
- Keskar et al. (CTRL), arXiv:1909.05858, 2019 (preprint)
- Deng et al., *ECCV* 2020. arXiv:2007.09580
- Suvorov et al. (LaMa), *WACV* 2022. arXiv:2109.07161
- Bài probe gần nhất: arXiv:2508.04567 (venue **UNVERIFIED**)

Tính mới của Mệnh đề 1 trong captioning và trong PU đa người gán: **UNVERIFIED**, cần một lượt tìm kiếm có mục tiêu ("multi-annotator positive-unlabeled propensity", "zero-inflated annotator mention").
