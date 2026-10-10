# R2_02: Phản biện vòng 2, trục METRIC M1–M3 (trùng lặp + tính đúng đắn toán học)

Phạm vi: mục 3 của `00_KE_HOACH.md` (M1 ViVG-P/R, M2 ViRHR + PDG, M3 H-R + SFA), đối chiếu định nghĩa chi tiết ở `02_graph_metrics.md` (M1, M2, M4 của file đó) và `11_relation_hallucination.md` (PDG). Ngày rà: 2026-10-10. Mọi bài dưới đây đã mở trang abs/HTML/proceedings trong phiên này, trừ chỗ ghi "Chưa xác minh".

---

## 1. Kết luận theo thành phần

| Thành phần | Trùng lặp | Tính đúng đắn | Kết luận |
|---|---|---|---|
| M1: gold 3 trạng thái | **Cao hơn plan khai**: đã có nhãn "unknown/unsure" trong gold caption (M-HalDetect, HalDec-Bench) | ổn nếu trạng thái do người gán | **needs-fix** (bỏ claim, sửa trích dẫn) |
| M1: precision dạng khoảng | Chưa thấy ở metric caption; có tiền lệ ở IR (đánh giá với phán đoán thiếu) và CuRe (credit có chặn cho claim ngoài tham chiếu) | **Lỗi**: định nghĩa plan và file 02 mâu thuẫn; khoảng loại ABS nên không phải cận thật; kiểm định "P_true nằm trong khoảng" gần như tự đúng; không xếp hạng được bằng khoảng | **needs-fix** |
| M1: phụ thuộc cha–con (INH) | DSG, 2604.01460 (đã biết) | **Gian lận được**: bịa object làm biến mất lỗi con khỏi mẫu số | **needs-fix** |
| M1: recall trọng số độ nổi bật | – | w(x) chưa định nghĩa; R_w khớp hypernym một chiều nên trùng/xung đột với H-R | **needs-fix** |
| M2: ViRHR (có điều kiện đầu mút) + RSR | Tri-HE, Reefknot, R-Bench (đã biết); không thấy bản caption tự do tiếng Việt | **Gian lận được**: mẫu số phụ thuộc hệ thống; vị từ mơ hồ ("ở gần", "có") gần như luôn đúng | **needs-fix** |
| M2: PDG | CDH-Bench RPD (QA), VLind-Bench (có thí nghiệm ảnh trắng), SumGD (so phân phối có/không ảnh trên caption), blank-image contrastive decoding | **Lỗi định nghĩa**: plan (ảnh trắng) ≠ file 11 (precision π cao − π thấp); "tỷ lệ chấp nhận trên ảnh trắng" không xác định cho caption tự do | **fail** ở dạng hiện tại → định nghĩa lại |
| M3: H-R | Taxonomy-Aware Eval (CVPR'25) đã áp hP/hR cho **văn bản tự do của VLM**, không chỉ "phân loại" như plan viết; Deng 2012 dùng information gain theo phân cấp | IC từ tần suất caption có thiên kiến báo cáo; DAG đa cha chưa xử lý; phía precision tổ tiên = TP toàn phần → nói chung chung được thưởng | **needs-fix** |
| M3: SFA | Chưa thấy metric diện tích cho caption; khung đã có: đường cong độ chính xác–độ cụ thể (Deng 2012), risk–coverage (Geifman 2017), Pareto factuality–coverage (ReflectCAP), "chơi an toàn" (2609.01888) | **Gian lận được**: thêm điểm θ chỉ có thể tăng diện tích; núm θ khác nhau giữa họ hệ thống nên không so được; hệ một điểm không có SFA | **needs-fix** (đổi sang toán tử lùi hậu kiểm chung) |

Đếm: **BLOCKER 4 (F1, F2, F4, F7), MAJOR 7, MINOR 4**.

---

## 2. Phát hiện

### F1. [BLOCKER] Định nghĩa M1 trong plan và trong file 02 mâu thuẫn; khoảng hiện tại không phải cận thật
- **Claim (plan §3):** "precision là *khoảng* [strict, lenient] theo node UNCERTAIN".
- **Thực tế (02, M1):** phần tử khớp node U được gán ABS và **loại khỏi cả tử và mẫu**; khoảng [P_lo, P_hi] chỉ chạy trên UNK (claim không khớp gì trong gold). Như vậy khoảng *không* "theo node UNCERTAIN" như plan viết, và vì ABS bị loại, độ chính xác thật trên toàn bộ claim có thể nằm **ngoài** [P_lo, P_hi].
- **Hệ quả gian lận:** hệ thống học cách nói về vùng mơ hồ (vật nhỏ, tối, bị che, giới tính không rõ) có claim rơi vào U → không bị tính. ViHG-Cap được huấn luyện quanh chính ranh giới U nên lợi thế này là thiên vị có hệ thống.
- **Sửa (định nghĩa chính xác, kiểu cận Manski cho dữ liệu thiếu):** với N = TP + FP + UNK + ABS (chưa tính INH, xem F3):
  - `P_lo = TP / N`
  - `P_hi = (TP + UNK + ABS) / N`
  - Độ rộng `W = (UNK + ABS)/N` báo riêng, tách hai phần `W_unk` (gold thiếu) và `W_abs` (gold không quyết được).
  - Thay câu trong plan: "precision là khoảng [P_lo, P_hi], trong đó cả claim không khớp gold (UNK) lẫn claim khớp node UNCERTAIN (ABS) được coi lần lượt là sai (cận dưới) và đúng (cận trên)."

### F2. [BLOCKER] Khoảng không xếp hạng được, nhưng T4 và meta-eval cần một số
- **Claim:** T4 "τ_c của M1 không kém VLM-judge quá 0,03"; 02 yêu cầu "luôn báo theo cặp, không gộp".
- **Vấn đề:** Kendall τ cần một điểm số cho mỗi caption/hệ thống. Hai khoảng chồng nhau không có thứ tự. Kiểm định đề xuất ở 02 ("P_true nằm trong [P_lo,P_hi] ở ≥90% hệ thống × lớp") **gần như tự đúng**: nếu nhãn S/N của gold đúng thì mọi tỉ lệ đúng của UNK ∈ [0,1] đều cho P_true trong khoảng; kiểm định chỉ bắt lỗi nhãn S/N, không đo gì về độ đầy đủ.
- **Sửa:**
  1. Định nghĩa điểm ước lượng `P̂ = (TP + q̂_u·UNK + q̂_a·ABS)/N`, với q̂_u, q̂_a là tỉ lệ đúng do **người chấm trên mẫu ngẫu nhiên 50 claim UNK và 50 claim ABS mỗi hệ thống**, kèm CI bootstrap. q̂ **theo từng hệ thống** (hệ cụ thể hơn sinh UNK có q thấp hơn; dùng một q chung sẽ thiên vị).
  2. T4 dùng P̂ (chính) và P_lo (phụ). Ghi rõ trong plan: "M1 xếp hạng bằng P̂; khoảng [P_lo,P_hi] là chẩn đoán độ đầy đủ gold."
  3. Thay kiểm định "P_true trong khoảng" bằng: (a) tương quan W với độ đầy đủ gold do người đánh giá; (b) báo q̂ theo hệ thống để cho thấy khoảng lệch về phía nào.
- Tiền lệ cần trích: IR đã xử lý phán đoán thiếu từ lâu (Buckley & Voorhees, *Retrieval Evaluation with Incomplete Information*, SIGIR 2004, bpref); CuRe (arXiv 2607.05150, 07/2026, video caption RL, không ghi venue) cho claim "được video ủng hộ nhưng không có trong tham chiếu" credit có chặn w_u = 0,5 — đây chính là phiên bản điểm của P_ver/q̂. Điểm khác còn lại của M1: **cận dưới/trên tường minh + q̂ đo bằng người**, không phải hằng số chọn tay.

### F3. [MAJOR] Quy tắc INH (loại con của cha sai khỏi mẫu số) cho phép giấu lỗi
- **Claim (02, M1):** "Phần tử INH bị loại khỏi tử số và mẫu số của số đo primary."
- **Phản ví dụ:** caption bịa "con chó" kèm "màu nâu", "đang nằm trên ghế", "đeo vòng cổ". Theo quy tắc, chỉ 1 FP (con chó); 3 claim con biến mất. Một hệ khác nói đúng "con mèo" nhưng sai màu bị 1 FP trên 2 claim. Hệ bịa nhiều hơn lại có precision tốt hơn. DSG dùng phụ thuộc để **không hỏi** câu vô nghĩa, không phải để tính precision của văn bản người đọc thấy.
- **Sửa:** P_lo và P̂ tính INH là FP (người đọc nhận cả 4 thông tin sai). Báo thêm `P_root` (chỉ object, không INH) và tỉ lệ `INH/N` như chỉ số "lỗi lan truyền". Đổi câu trong 02: "INH được tính là sai trong precision tổng hợp và báo riêng khối lượng."

### F4. [BLOCKER] "Gold 3 trạng thái" không mới và có nguy cơ vòng lặp tự phục vụ
- **Claim (plan §1, §3):** "DSG/PoSh/CAPTURE: tất cả gold nhị phân"; "chưa thấy gold ba trạng thái".
- **Bằng chứng:**
  - M-HalDetect (Gunjal et al., arXiv 2308.06394, AAAI 2024): nhãn đoạn dưới câu Accurate / Inaccurate / Analysis / **Unsure**.
  - HalDec-Bench (Saito et al., arXiv 2511.20515 v4, 03/2026, chưa ghi venue): nhãn câu **correct / incorrect / unknown**, "unknown" khi vật quá nhỏ hoặc thuộc tính không nhìn thấy, và **loại unknown khỏi đánh giá**, tức đúng cách ABS của 02. (Đã đọc trong HTML v4.)
- **Rủi ro vòng lặp:** plan §4 gán gold SG "máy gợi ý → người sửa". Nếu trạng thái S/U/N được gợi ý bởi chính verifier VSPS (Vintern) đã sinh G* để huấn luyện ViHG-Cap, người sửa bị neo vào trạng thái máy; ViHG-Cap sẽ được chấm trên ranh giới U mà nó được dạy.
- **Sửa:**
  1. Xóa "tất cả gold nhị phân" và "chưa thấy gold ba trạng thái". Viết: "Nhãn 'unknown' đã có ở cấp câu (M-HalDetect, HalDec-Bench) và thường bị loại khỏi đánh giá; chúng tôi giữ nó ở cấp node/cạnh của đồ thị và đưa vào cận precision thay vì loại bỏ."
  2. Trạng thái S/U/N trên gold test do người gán **không thấy** trạng thái của verifier (chỉ được thấy node/box gợi ý). Trên ≥100 ảnh, gán mù hoàn toàn và báo κ giữa "có gợi ý" và "mù"; nếu κ < 0,7 thì toàn bộ gold phải gán mù.
  3. Ghi trong plan: "Verifier VSPS chỉ dùng cho silver/huấn luyện, không bao giờ quyết định trạng thái gold."

### F5. [MAJOR] Tổ tiên được tính TP toàn phần ở precision → nói chung chung đạt precision ~1
- **Claim (02, M4 = H-R của plan):** "c là tổ tiên của g: đúng về precision (TP)". M1 khớp ở tầng LEXICAL với hypernym một chiều (`chair.py`).
- **Phản ví dụ** (gold: phụ nữ S, áo dài S, xe máy S, ⟨phụ nữ, ngồi trên, xe máy⟩ S):
  - A: "người phụ nữ mặc áo dài đỏ ngồi trên xe máy" (màu là FP): P_lo = 4/5.
  - B: "một người ở gần một chiếc xe": người ⊑ phụ nữ, xe ⊑ xe máy, "ở gần" ⊑ "ngồi trên" theo thang vị từ của plan → P_lo = 3/3 = 1,0.
  - B thắng precision; chỉ H-R phạt B. Nhưng R_w của M1 (khớp LEXICAL + hypernym) lại cho B credit **toàn phần** cho "người", nên M1 và M3 cho hai số recall mâu thuẫn trên cùng claim.
- **Sửa:**
  1. M1-R_w chỉ khớp đồng nghĩa/chính xác; khớp tổ tiên chỉ được tính trong H-R. Ghi: "R_w là recall chính xác; H-R là phiên bản có credit một phần; không khớp tổ tiên trong R_w."
  2. Thêm tập **khái niệm rỗng nghĩa** V (gốc phân cấp: vật, đồ vật, thứ, cái; vị từ: có, với, ở gần, cạnh) gồm các khái niệm có p(c) cộng dồn ≥ 0,5 hoặc độ sâu ≤ 1. Claim thuộc V không vào tử số TP mà báo riêng `VacR = #V/N`.
  3. Luôn báo kèm **độ cụ thể trung bình của claim đúng** `MSI = mean_{TP} IC(c)/IC_max`. Precision không được báo một mình.

### F6. [MAJOR] ViRHR: mẫu số phụ thuộc hệ thống, gian lận bằng vị từ mơ hồ
- **Claim:** "Tỷ lệ ảo giác quan hệ, chỉ tính khi cả hai đầu đúng".
- **Vấn đề:**
  1. Hệ bịa object nhiều có ít quan hệ "đánh giá được" hơn → RHR tính trên tập con dễ hơn; hai hệ không so được nếu không biết độ phủ.
  2. "ở gần", "cạnh", "có" gần như luôn S → RHR thấp nhờ vị từ rỗng nghĩa (cùng cơ chế F5).
  3. RSR (đổi vai) không xác định với vị từ đối xứng (cạnh, gần, cùng với): chiều ngược cũng S → bị đếm là đổi vai.
- **Sửa:**
  - Báo cặp (RHR, `EvalCov = #đánh giá được/#quan hệ`); so sánh hệ thống chỉ trên **giao** các ảnh/cặp object mà mọi hệ đều có đầu mút TP (hoặc báo cả hai).
  - Áp F5 cho vị từ: vị từ trong V không tính vào mẫu RHR, báo `VacRel`; báo **H-R_rel** (recall phân cấp cho vị từ theo thang ~30 vị từ ở file 11).
  - RSR: mẫu số chỉ gồm vị từ bất đối xứng (đánh dấu trong bảng canonical).

### F7. [BLOCKER] PDG không xác định cho caption tự do và mâu thuẫn giữa các file
- **Claim (plan):** "PDG = chênh tỷ lệ chấp nhận quan hệ 'quen thuộc' vs 'lạ' giữa ảnh thật và ảnh trắng". **File 11:** "precision ở bộ ba π cao trừ precision ở bộ ba π thấp" (bản caption của RPD trong CDH-Bench).
- **Vấn đề:**
  1. Trên ảnh trắng, captioner nói "ảnh trắng/không có gì" → không có quan hệ để "chấp nhận". Khái niệm "tỷ lệ chấp nhận" chỉ tồn tại ở chế độ hỏi có/không (tức đo **verifier**, không đo captioner).
  2. Bản file 11 bị nhiễu: bộ ba π thấp vốn hiếm, khó, gold kém đầy đủ hơn; chênh precision không tách được "dựa vào prior" khỏi "độ khó". CDH-Bench tránh điều này bằng **ảnh cặp đối chứng** (ảnh phản thường thức vs ảnh thường thức, RPD = CFAD/CS-Acc, chỉ QA, không dùng ảnh trắng; đã đọc HTML v2).
  3. Đo ảnh trắng không mới: VLind-Bench (Findings NAACL 2025) có phụ lục dùng ảnh trắng; SumGD (Min et al., arXiv 2410.13321, Findings NAACL 2025) so phân phối token có/không ảnh trên chính caption; arXiv 2512.19070 dùng ảnh trắng cho contrastive decoding.
- **Sửa: định nghĩa chính xác hai thành phần, chọn một làm chính:**
  - **PDG_tf (chính, mô hình mở trọng số):** với mỗi quan hệ r̂ trong caption của mô hình, teacher-forcing tiền tố, tính `Δ(r̂) = log p(r̂ | I, prefix) − log p(r̂ | I_∅, prefix)`, với I_∅ ∈ {ảnh trắng, ảnh trung bình tập, ảnh mờ Gauss} (báo cả ba). Quan hệ "do prior" khi Δ < δ (δ cố định trước, ví dụ 0,5 nat). `PDG_tf = Pr(FP | Δ<δ) − Pr(FP | Δ≥δ)` và `PriorShare = Pr(Δ<δ)`. Điểm khác so với SumGD: tính trên **đơn vị quan hệ có nhãn gold**, tách FP/TP.
  - **PDG_cf (phụ):** chỉ trên tập con ViRel-300 có quan hệ π thấp thật (60 ảnh của file 11), ghép mỗi ảnh π thấp với một ảnh π cao cùng cặp object: `PDG_cf = (Prec_highπ − Prec_lowπ)/Prec_highπ`, ghi rõ là bản caption của RPD (CDH-Bench).
  - Xóa cụm "giữa ảnh thật và ảnh trắng" khỏi plan, hoặc thay bằng định nghĩa PDG_tf. Bỏ claim "R-Bench, Reefknot: không đo trên caption" làm điểm khác duy nhất; thêm SumGD/VLind/CDH-Bench vào cột "gần nhất".
  - Thống kê: π chia tertile **trước khi** chạy (theo tần suất trong caption train KTVIC đã parse), bootstrap theo ảnh; nếu một bin < 100 quan hệ thì không báo.

### F8. [MAJOR] "Taxonomy-Aware Eval chỉ đánh giá phân loại" là mô tả sai, làm phồng tính mới của H-R
- **Claim (plan §3 M3):** "Taxonomy-Aware Eval CVPR'25 (chỉ đánh giá phân loại)".
- **Bằng chứng:** Snæbjarnarson et al., arXiv 2504.05457, CVPR 2025: khung đánh giá **văn bản dự đoán không ràng buộc của VLM** bằng hierarchical precision/recall sau khi ánh xạ văn bản vào taxonomy. Nhiệm vụ là phân loại chi tiết (một nhãn/ảnh), nhưng cơ chế credit một phần cho văn bản tự do đã có. Thêm: Deng et al., *Hedging Your Bets*, CVPR 2012, đã tối ưu đánh đổi độ chính xác–độ cụ thể với phần thưởng information gain theo phân cấp (tương đương IC).
- **Sửa:** Viết lại cột "gần nhất/khác biệt" của M3: "hP/hR cho văn bản VLM đã có (Taxonomy-Aware Eval, một nhãn/ảnh); đánh đổi độ chính xác–độ cụ thể theo phân cấp đã có cho phân loại (Deng 2012). Khác biệt: nhiều thực thể + quan hệ trong một caption, căn instance, kết hợp với precision dạng khoảng, tiếng Việt." Ablation bắt buộc: credit theo IC so với credit theo độ dài đường đi chung (công thức của Taxonomy-Aware Eval); nếu không khác về tương quan người thì dùng bản đường đi (đơn giản hơn, có tiền lệ).

### F9. [MAJOR] Định nghĩa IC của H-R thiếu chặt
- **Vấn đề:**
  1. p(c) lấy từ tần suất **caption** KTVIC: đo thói quen báo cáo, không đo thông tin thị giác ("người" cực phổ biến → IC rất thấp, credit "người" cho gold "phụ nữ" có thể ~0,1–0,3, phạt nặng chính chiến lược VSPS/ViHG-Cap đề xuất).
  2. Wikidata P279 là DAG đa cha; đếm cộng dồn bị đếm trùng, IC(cha) có thể không đơn điệu theo đường đi đã chọn.
  3. IC(g) = 0 khi g ở gốc → chia cho 0.
- **Sửa:** cây hóa phân cấp (mỗi khái niệm một cha chính trong bảng ~250 dòng; đa cha chỉ giữ cha chính), p(c) cộng dồn trên cây đó, `credit(c,g) = IC(c)/IC(g)` nếu c ⊑ g và IC(g) > 0, ngược lại 1 nếu c ≡ g; credit = max trên các cách khớp. Báo độ nhạy: p(c) từ caption KTVIC vs từ nhãn object (VietSGG/VG ánh xạ). Kiểm định người 100 cặp khái niệm (đã có ở 02) phải chạy **trước** khi chốt nguồn p(c).

### F10. [MAJOR] SFA gian lận được và không so được giữa họ hệ thống
- **Claim (plan + 02):** SFA = hypervolume 2D của đường bao Pareto các điểm (H-R(θ), P_lo(θ)) khi quét núm θ của từng họ; hệ một điểm thì không báo SFA.
- **Vấn đề:**
  1. Hypervolume **không giảm** khi thêm điểm → họ có nhiều mức θ hơn luôn có SFA ≥.
  2. θ khác nhau (ngưỡng verifier, độ dài, ngân sách entity) → miền quét khác nhau, diện tích không cùng thước.
  3. Hầu hết baseline (zero-shot, GRIT, FoCUS-style) là một điểm → SFA chỉ áp cho chính phương pháp của mình: metric không so được với ai.
  4. arXiv 2609.01888 (*Does Playing it Safe Count as Faithfulness?*, 09/2026, chưa ghi venue) cho thấy nhiều phương pháp giảm ảo giác chỉ trượt dọc "đường chéo chơi an toàn" (giảm recall/độ chi tiết). Reviewer sẽ hỏi ngay: ViHG-Cap có hơn **baseline + lùi IsA hậu kiểm** không?
- **Sửa (định nghĩa chính xác):**
  - Toán tử lùi hậu kiểm chung `B_k`: thay mọi node thực thể/vị từ trong đồ thị parse của caption bằng tổ tiên bậc k trên cây (dừng ở gốc; vị từ theo thang ~30 vị từ), k = 0..K, K = 3 cố định, cộng mức "bỏ" (k = ∞ → caption rỗng, loại khỏi đường cong vì P không xác định).
  - Với **mọi** hệ thống: điểm `(H-R(B_k), P̂(B_k))`, k=0..K; `SFA = diện tích dưới đường bậc thang Pareto` của K+1 điểm này trong [0,1]², tham chiếu (0,0). Mọi hệ cùng số điểm, cùng toán tử → so được, kể cả hệ một điểm.
  - Thử nghiệm bắt buộc trong P2: điểm k=0 của ViHG-Cap phải nằm **trên** đường cong B_k của baseline SFT tốt nhất (thắng về Pareto), không chỉ có SFA lớn hơn. Nếu nằm trên đường cong đó → ViHG-Cap chỉ tương đương lùi hậu kiểm, không được claim lõi phương pháp.
  - Trích dẫn tiền lệ khung: Deng 2012 (đường cong độ chính xác–độ cụ thể), Geifman & El-Yaniv NeurIPS 2017 (risk–coverage), ReflectCAP arXiv 2604.12357 (biên Pareto factuality–coverage, không có diện tích). Tên đúng của đóng góp: "AUC đường cong lùi hậu kiểm cho caption", không phải "khái niệm đánh đổi mới".

### F11. [MAJOR] Trọng số độ nổi bật w(x) chưa định nghĩa
- **Claim:** "recall có trọng số độ nổi bật".
- **Vấn đề:** nếu w lấy từ tần suất đề cập trong caption mô hình hoặc từ verifier thì vòng lặp; nếu chọn tay thì tùy tiện.
- **Sửa:** `w(x) = (1 + #tham chiếu người trong 5 caption KTVIC/UIT có đề cập x hoặc hậu duệ của x) / 6`, cố định trước, ablation w ≡ 1. Ghi rõ trong bảng M1.

### F12. [MINOR] Đánh số metric không khớp giữa plan và file 02
Plan M3 (H-R/SFA) = 02 M4; 02 M3 (PHS/KCV) không có trong plan. Sửa: thêm dòng chú thích ánh xạ ở đầu §3, hoặc đổi số trong 02.

### F13. [MINOR] "Trái/phải mặc định U" (02, M2) kết hợp ABS bị loại → mọi quan hệ trái/phải miễn phí
Sau F1 (ABS vào cận), điều này tự hết. Nếu không sửa F1 thì phải gán trái/phải theo hình học box thay vì U mặc định.

### F14. [MINOR] Chống gian lận bằng độ dài/liệt kê ở phía recall
Liệt kê mọi object có thể có làm R_w và H-R tăng, P giảm; đã báo cặp P/R nên chấp nhận được, nhưng cần thêm một dòng: "không báo R mà không kèm P̂ và số claim/caption", như OmniCapBench (arXiv 2610.12458, NeurIPS 2026 theo comment) lập luận rằng đánh giá một chiều có thể bị gian lận.

### F15. [MINOR] Kiểm định M1 qua ablation "mỗi thành phần phải làm τ tăng có ý nghĩa"
Với 500 ảnh và 5 hệ, cấp hệ thống chỉ có 5 điểm, nên τ cấp hệ thống không có sức mạnh thống kê. Ghi: kiểm định thành phần ở **cấp caption** (Williams/bootstrap), cấp hệ thống chỉ báo mô tả.

---

## 3. Những gì plan làm đúng
- Tách P/R, không gộp; báo theo loại O/A/R; có ablation từng thành phần metric.
- Nhận ra "gold không đầy đủ" là vấn đề thật và muốn biểu diễn nó tường minh; ý tưởng cận precision chưa thấy ở metric caption nào trong lần rà này (HalDec-Bench, M-HalDetect chỉ loại unknown).
- ViRHR có điều kiện theo đầu mút để tách lỗi object khỏi lỗi quan hệ là đúng hướng (Tri-HE không tách); RSR là chẩn đoán hữu ích.
- H-R có động cơ phương pháp thật: recall phẳng phạt việc lùi IsA một cách không công bằng.
- SFA nhận ra hệ một điểm không có thông tin; chỉ cần đổi sang toán tử lùi chung (F10) là dùng được cho mọi hệ.
- Có cổng T4 hạ M1 xuống "chẩn đoán" nếu thua VLM-judge.

## Nguồn đã mở trong phiên
- Taxonomy-Aware Evaluation of VLMs, arXiv 2504.05457 (CVPR 2025): https://arxiv.org/abs/2504.05457
- HalDec-Bench, arXiv 2511.20515 v4 (nhãn correct/incorrect/unknown, loại unknown): https://arxiv.org/html/2511.20515v4
- M-HalDetect, arXiv 2308.06394 (nhãn Unsure; nội dung nhãn lấy qua kết quả tìm kiếm, chưa mở PDF): https://arxiv.org/pdf/2308.06394
- CDH-Bench, arXiv 2603.27982 v2 (RPD = CFAD/CS-Acc, QA, không ảnh trắng): https://arxiv.org/html/2603.27982v2
- VLind-Bench, Findings NAACL 2025: https://aclanthology.org/2025.findings-naacl.231.pdf
- SumGD, arXiv 2410.13321 (Findings NAACL 2025): https://arxiv.org/abs/2410.13321
- Blank-image contrastive decoding, arXiv 2512.19070 (chi tiết chưa mở): https://arxiv.org/html/2512.19070
- CuRe, arXiv 2607.05150 (credit có chặn w_u = 0,5): https://arxiv.org/html/2607.05150
- Does Playing it Safe Count as Faithfulness?, arXiv 2609.01888: https://arxiv.org/abs/2609.01888
- ReflectCAP, arXiv 2604.12357: https://arxiv.org/abs/2604.12357
- OmniCapBench, arXiv 2610.12458 (NeurIPS 2026 theo comment): https://arxiv.org/abs/2610.12458
- Reinforcing Consistency in Video MLLMs with Structured Rewards, arXiv 2604.01460 (COLM 2026): https://arxiv.org/abs/2604.01460
- Deng et al., Hedging Your Bets, CVPR 2012: https://mlanthology.org/cvpr/2012/deng2012cvpr-hedging
- Geifman & El-Yaniv, Selective Classification for DNNs, NeurIPS 2017: https://arxiv.org/abs/1705.08500
- Buckley & Voorhees, Retrieval Evaluation with Incomplete Information, SIGIR 2004: https://ir.webis.de/anthology/2004.sigirconf_conference-2004.5/
- Ngoài phạm vi trục này nhưng cần trục "lùi IsA" xem: HFRU arXiv 2605.08031 (phần thưởng thay khái niệm bằng khái niệm cha khi unlearning; chi tiết chưa xác minh).
