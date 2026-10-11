# R2-04: Trinh sát frontier 2025–2026 và 4 ý tưởng mới cho captioning tiếng Việt

**Tóm tắt (5 dòng)**
1. Mặt trận 2025–2026 xoay quanh ba chủ đề: phần thưởng có thể kiểm chứng cho caption (CapRL, RubiCap, SC-Captioner), đánh giá bằng QA hoặc theo đơn vị thông tin (CAPTURE, DCScore, CapArena, CaptionQA), và captioner biết "suy nghĩ" hoặc biết grounding (VideoCap-R1, DAM, Aurora).
2. Mọi thứ trên đều làm bằng tiếng Anh, cho caption **dày**, và mặc định "nói nhiều hơn là tốt hơn". Tôi không tìm thấy bài nào áp dụng chúng cho tiếng Việt hay cho caption **ngắn** có 5 tham chiếu (KTVIC).
3. Từ các khoảng trống đó, tôi đề xuất 4 ý tưởng: (I1) chọn nội dung tối ưu Bayes dưới phân phối người gán; (I2) loại từ tiếng Việt làm điểm cam kết để kiểm chứng; (I3) "kiểm kê rồi chọn", huấn luyện trên tham chiếu người đã lọc trung thực; (I4) trục thứ ba, *mức gọi tên*, tức tên cấp nhập môn kiểu Việt.
4. Mỗi ý tưởng có thí nghiệm bác bỏ được, tốn ≤3 GPU-giờ trên một 3090, và phần lớn dùng lại `data/stage1_records` cùng các output sẵn có.
5. I1 và I4 bổ sung trực tiếp cho Know-and-Mention (KaM). I3 cạnh tranh một phần với KaM ở khâu tạo mục tiêu SFT. I2 trực giao với KaM, đóng vai cơ chế ở thời điểm suy luận.

Quy ước: "Chưa làm cho tiếng Việt" nghĩa là tôi đã tìm và không thấy (WebSearch, 10/2026). Điều đó không chứng minh là không tồn tại. Venue chưa xác nhận được thì ghi UNVERIFIED.

---

## 1. Bản đồ xu hướng

| Xu hướng | Bài chính (venue, link) | Họ được gì | Đã có cho tiếng Việt? |
|---|---|---|---|
| RL với phần thưởng kiểm chứng được cho caption | **CapRL**, ICLR 2026, [2509.22647](https://arxiv.org/abs/2509.22647). Một LLM không nhìn ảnh trả lời MCQ chỉ từ caption, và độ chính xác đó là reward cho GRPO. **CapRL++**, arXiv 2026, [2606.09393](https://arxiv.org/abs/2606.09393), venue UNVERIFIED, mở rộng sang video | Trong khung Prism, CapRL ngang Qwen2.5-VL-72B và hơn baseline trung bình 8,4% | Không thấy |
| Phần thưởng dạng rubric do LLM viết | **RubiCap**, arXiv 03/2026, [2603.09160](https://arxiv.org/abs/2603.09160), venue UNVERIFIED | Win-rate cao nhất trên CapArena. Bản 7B ngang Qwen2.5-VL-32B trên CaptionQA | Không thấy |
| Tự sửa lỗi hoặc tự cải thiện bằng RL | **SC-Captioner**, ICCV 2025, [2508.06125](https://arxiv.org/abs/2508.06125). Reward là hiệu giữa scene graph trước và sau khi sửa, đối chiếu với tham chiếu | Vượt DPO. Họ nêu rõ bài toán là đánh đổi P/R theo độ dài | Không thấy |
| Captioner "suy nghĩ" (think-then-caption) | **VideoCap-R1**, arXiv [2506.01725](https://arxiv.org/abs/2506.01725), venue UNVERIFIED: suy nghĩ có cấu trúc rồi caption, GRPO với 2 reward. **Visionary-R1**, [2505.14677](https://arxiv.org/abs/2505.14677): caption → lý luận → trả lời | VideoCap-R1 cải thiện 7B chỉ với 1,5k video. SFT trên phần "thinking" thì *không* giúp, chỉ RL mới giúp | Không thấy |
| Test-time scaling cho tri giác | **VisRef**, [2603.00207](https://arxiv.org/abs/2603.00207): lý luận dài làm trôi khỏi token ảnh. **HoneyBee**, [2510.12225](https://arxiv.org/abs/2510.12225) | Chưa có bài TTS nào dành riêng cho captioning. Bằng chứng còn cho thấy lý luận dài *hại* tác vụ thiên về tri giác | Không thấy |
| Đa tác tử | **Lee et al.**, ICML 2025, [2412.15484](https://arxiv.org/abs/2412.15484): LLM và MLLM phối hợp để sửa caption | Ảo giác tăng theo độ dài vì mô hình dựa vào chữ nó đã sinh hơn là vào ảnh. Họ đề xuất metric kép factuality/coverage | Không thấy |
| Caption theo vùng, có grounding | **Describe Anything (DAM)**, ICCV 2025, [2504.16072](https://arxiv.org/abs/2504.16072) | SOTA trên 7 benchmark caption cục bộ. DLC-Bench chấm điểm không cần tham chiếu | Không thấy |
| Perception tokens | **Aurora**, CVPR 2025, [2412.03548](https://arxiv.org/abs/2412.03548): sinh token depth hoặc box làm bước trung gian | +10,8% BLINK-counting, +11,3% CVBench-counting | Không thấy |
| Đánh giá theo đơn vị hoặc bằng QA | **CAPTURE**, [2405.19092](https://arxiv.org/abs/2405.19092), venue UNVERIFIED. **DCScore**, ICLR 2025, [2503.07906](https://arxiv.org/abs/2503.07906). **CapArena**, ACL Findings 2025, [2503.12329](https://arxiv.org/abs/2503.12329). **CaptionQA**, CVPR 2026, [2511.21025](https://arxiv.org/abs/2511.21025) | CapArena: METEOR khớp với người ở mức từng caption nhưng xếp hạng mô hình sai; VLM-as-judge tương quan 93,4% với xếp hạng của người. CaptionQA: các mô hình ngang nhau trên VQA vẫn chênh tới 32% về "tiện ích caption" | Không thấy |
| Caption dày và caption ngắn khi tái caption | **Lai et al.**, [2410.02740](https://arxiv.org/abs/2410.02740), ICLR 2025 theo trang Apple ML Research | Mỗi mô hình ưa một định dạng caption riêng. Lai kết hợp caption tổng hợp với alt-text gốc thì tốt hơn chỉ dùng caption tổng hợp | Không thấy |
| Nhận thức văn hóa, ngôn ngữ ít tài nguyên | **MELLA**, [2508.05502](https://arxiv.org/abs/2508.05502), được liệt kê ở IJCAI 2026 (UNVERIFIED). **Pangea**, ICLR 2025, [2410.16153](https://arxiv.org/abs/2410.16153) | MELLA: alt-text bản địa giảm "ảo giác văn hóa", tức là gọi sai hoặc bỏ sót thực thể đặc thù, điều mà dữ liệu dịch máy không làm được | MELLA gồm 8 ngôn ngữ, danh sách đầy đủ UNVERIFIED |
| "Biết nhiều hơn điều nói ra" | [2508.04567](https://arxiv.org/abs/2508.04567): probe tuyến tính đạt trên 95% về sự tồn tại của đối tượng, trong khi phần sinh chỉ khoảng 81% | Họ sửa LM head chứ không dựng mục tiêu SFT | Không thấy |

Phía tiếng Việt hiện chỉ có dataset và mô hình nền: KTVIC ([2401.08100](https://arxiv.org/abs/2401.08100)), UIT-OpenViIC ([2305.04166](https://arxiv.org/abs/2305.04166)), Vintern-1B ([2408.12480](https://arxiv.org/abs/2408.12480)), VMMU ([2508.13680](https://arxiv.org/abs/2508.13680), về lý luận chứ không phải caption) và ViCLIP-OT (2602.22678, retrieval). Tôi không tìm thấy bài nào về RLVR, đánh giá bằng QA, thinking captioner hay đo ảo giác cho caption tiếng Việt.

## 2. Khoảng trống rút ra (không phải ghép bài)

- **G1. Frontier tối ưu sai đại lượng cho caption ngắn.** Reward QA (CapRL, CaptionQA) và rubric (RubiCap) thưởng cho *độ bao phủ*, nên về bản chất nghiêng về recall. KTVIC có 5 tham chiếu ngắn, và 38% đối tượng gold chỉ được 1/5 người nhắc. Ở đây câu hỏi không phải "nói thêm gì" mà là "chọn gì dưới bất định giữa những người gán". Chưa ai coi 5 tham chiếu là *mẫu từ một phân phối*, rồi giải bài toán chọn nội dung như một quyết định tối ưu với phân phối đó.
- **G2. Mọi thứ đều được thiết kế theo tiếng Anh.** Không phương pháp nào khai thác cấu trúc ngữ pháp của ngôn ngữ đích. Tiếng Việt có **loại từ** (chiếc, con, cái, bức, ngôi...) đứng *trước* danh từ, nên mô hình phải cam kết một lớp phân loại trước khi gọi tên. Tôi đếm trên 18.845 caption train của KTVIC: trung bình 0,57 loại từ mỗi caption (chiếc 2.721, bức 1.439, cái 1.327, con 1.200...). Phép đếm thô, không có POS, nên lẫn "con sông" và "cây" với nghĩa danh từ.
- **G3. Thinking captioner chỉ phục vụ caption dày.** VideoCap-R1 cho thấy SFT trên phần thinking không giúp, và VisRef cho thấy lý luận dài làm trôi khỏi ảnh. Chưa ai dùng bước "suy nghĩ" như một **bản kiểm kê tri giác có ràng buộc** để rồi *chọn* ra caption ngắn, với văn phong người làm đầu ra.
- **G4. Văn hóa = gọi đúng tên ở đúng mức.** MELLA cho thấy ảo giác văn hóa là gọi sai hoặc bỏ sót thực thể đặc thù. CIDEr dùng TF-IDF nên thưởng mạnh cho n-gram hiếm mà nhiều người gán cùng dùng. Đó chính là các tên đặc thù kiểu "nón lá" hay "xe ba gác", trái với tên chung "cái mũ" hay "chiếc xe". Bài toán *mức gọi tên* (entry-level, [Ordonez et al., ICCV 2013](https://openaccess.thecvf.com/content_iccv_2013/html/Ordonez_From_Large_Scale_2013_ICCV_paper.html)) chưa từng được đặt ra cho VLM hay cho tiếng Việt.

## 3. Bốn ý tưởng

### I1. Caption tối ưu Bayes dưới phân phối người gán ("Plural-Optimal Captioning")

**Luận điểm.** Một caption ngắn tốt là **quyết định Bayes** tối đa hóa F1 và CIDEr *kỳ vọng* so với một người gán ngẫu nhiên chưa thấy. Nó không phải bản bắt chước một tham chiếu. Với xác suất biên p_i = P(tồn tại) × P(nhắc | tồn tại), tập đối tượng tối ưu theo F1 kỳ vọng có lời giải chính xác bằng thuật toán General F-measure Maximizer (Dembczyński et al., NeurIPS 2011; link UNVERIFIED, cần kiểm trước khi trích). Ngưỡng tối ưu phụ thuộc vào từng ảnh và **không** cố định. Đây là giải thích hình thức vì sao một ngưỡng duy nhất (verifier) buộc phải đánh đổi.

**Vì sao chưa ai làm.** Văn liệu tối ưu F-measure thuộc về phân loại đa nhãn. Captioning frontier thì coi tham chiếu là đích để khớp (SFT, SCST) hoặc bỏ hẳn tham chiếu (CapRL). Chưa ai coi 5 tham chiếu là mẫu của một phân phối đề cập để rút ra *chính sách chọn nội dung tối ưu*. Cũng chưa ai chỉ ra rằng tính đồng thuận của CIDEr có cùng điểm tối ưu với F1 kỳ vọng, nên hai metric có thể tăng cùng nhau.

**Cơ chế.**
1. Ước lượng p_i từ hai trục của KaM.
2. Chọn tập đối tượng bằng GFM theo từng ảnh.
3. Render thành mục tiêu SFT, hoặc dùng làm reward GRPO "leave-one-annotator-out": điểm của caption tính trên 4 tham chiếu để dự đoán tham chiếu thứ 5. Đây là ước lượng không chệch của metric kỳ vọng.

**Thí nghiệm đầu, khoảng 0,5 GPU-giờ, chủ yếu CPU.**
1. Lấy mệnh đề Stage-1 trên tập dev.
2. Dùng p_exist từ logit verifier đã có (gate T0.5, κ = 0,79) và p_mention là tần suất lớp trong tham chiếu train.
3. So hai cách chọn tập: GFM và ngưỡng cố định tốt nhất, chọn ngưỡng trên dev.
4. Chấm object-F1 leave-one-out và CIDEr của caption template.

Bác bỏ nếu GFM không hơn ngưỡng cố định tốt nhất ít nhất 1,5 điểm F1, hoặc nếu CIDEr giảm.

**Rủi ro.** p_i có thể kém hiệu chuẩn, mà GFM nhạy với hiệu chuẩn. Ngoài ra, phần lý thuyết có thể bị reviewer coi là "áp dụng định lý cũ". Phần mới phải nằm ở hệ quả đo được: ngưỡng thay đổi theo ảnh và giải thích được đánh đổi.

### I2. Loại từ là điểm cam kết: kiểm chứng ở token loại từ ("Classifier Checkpoints")

**Luận điểm.** Trong tiếng Việt, mô hình chọn "con", "chiếc" hay "bức" *trước* khi chọn danh từ, tức là cam kết vào một lớp hữu sinh hay hình dạng. Độ bất định ở token loại từ là tín hiệu ảo giác **sớm hơn và rẻ hơn** tín hiệu ở danh từ. Vì vậy test-time compute chỉ cần chi ở những điểm này.

**Vì sao chưa ai làm.** Hướng TTS và phát hiện ảo giác ở frontier (HaloProbe, VisRef) đều đặt điểm kiểm tra theo token hoặc câu, không gắn với ngôn ngữ. Tôi không tìm thấy công trình nào dùng hệ loại từ của ngôn ngữ Đông Nam Á hay Đông Á làm điểm kiểm chứng ảo giác.

**Cơ chế.**
1. Khi giải mã, nếu xác suất loại từ hoặc logit probe tồn tại tại vị trí đó thấp, tách K=4 nhánh.
2. Chấm mỗi nhánh bằng logit verifier của danh từ theo sau, rồi giữ nhánh có đồng thuận MBR cao nhất với các mẫu khác để bảo toàn văn phong, nhờ đó CIDEr không giảm.
3. Chưng cất các lựa chọn đó vào SFT để suy luận vẫn chỉ một lượt.

**Thí nghiệm đầu, khoảng 1 GPU-giờ.**
1. Teacher-force các caption zero-shot của Qwen2.5-VL-7B trên dev hoặc gold.
2. Ghi entropy và hidden state tại loại từ và tại danh từ.
3. Gán nhãn danh từ có ảo giác hay không (bằng gold-300 nếu đã có, nếu chưa thì bằng SUPPORTED kết hợp tham chiếu).
4. So AUROC ở vị trí loại từ với AUROC ở vị trí danh từ.

Bác bỏ nếu AUROC tại loại từ ≤ AUROC tại danh từ + 0,02, hoặc nếu dưới 30% danh từ đối tượng có loại từ đi trước (0,57 loại từ mỗi caption cho thấy đây là rủi ro thật).

**Rủi ro.** Độ phủ thấp, vì "người", "xe máy" và nhiều danh từ không đi kèm loại từ. Đóng góp có thể chỉ dừng ở mức một phân tích hay. Khi đó vẫn có thể viết thành bài ngắn, kiểu "phân tích ngôn ngữ học cho ảo giác VLM tiếng Việt".

### I3. Kiểm kê rồi chọn, với tham chiếu người đã lọc trung thực ("Inventory-then-Select")

**Luận điểm.** VSPS mất CIDEr và BLEU vì mục tiêu SFT là caption dựng từ template. Zero-shot mất precision vì nó nói những gì không ai kiểm. Hướng giải là để mô hình **tự kiểm kê** các mệnh đề kèm cờ niềm tin (phần "thinking") rồi viết caption ngắn theo văn phong *người*, với ràng buộc là danh từ trong caption phải nằm trong bản kiểm kê. Mục tiêu SFT là **những tham chiếu người mà mọi đối tượng đều nằm trong bản kiểm kê đã kiểm chứng**. Trong 5 tham chiếu, chỉ những câu "trung thực với ảnh theo bằng chứng của chính mô hình" được giữ lại.

**Vì sao chưa ai làm.** Thinking captioner ở frontier sinh caption dày và cần RL mới có lợi (VideoCap-R1). Các hướng lọc tham chiếu thì lọc theo chất lượng ngôn ngữ, không lọc theo việc tham chiếu có được ảnh xác nhận qua chính mô hình hay không. Kết hợp "kiểm kê có ràng buộc" với "tham chiếu người được chọn bởi kiểm kê" giải đúng mâu thuẫn của VSPS: văn phong người kéo CIDEr lên, ràng buộc kiểm kê giữ precision.

**Cơ chế.**
1. Stage-1 có sẵn: mệnh đề kèm điểm kiểm chứng.
2. Với mỗi ảnh train, lọc 5 tham chiếu theo luật: đối tượng trong tham chiếu ⊆ (tập SUPPORTED ∪ tập có probe ≥ τ).
3. SFT với định dạng `<kiểm kê>…</kiểm kê> caption`.
4. Khi suy luận, bỏ caption nào chứa danh từ ngoài kiểm kê, hoặc ràng buộc từ vựng ngay lúc giải mã.

**Thí nghiệm đầu, khoảng 2,5 GPU-giờ.**
1. Thống kê trên CPU: tỷ lệ tham chiếu train qua được bộ lọc, và CIDEr của chúng so với các tham chiếu còn lại.
2. QLoRA một epoch trên khoảng 2k ảnh, so ba cấu hình: (a) toàn bộ tham chiếu, (b) tham chiếu đã lọc, (c) tham chiếu đã lọc kèm kiểm kê.
3. Chấm trên dev: CIDEr, BLEU-4, object P/R.

Bác bỏ nếu (c) không đạt đồng thời P ≥ 41,5 và CIDEr ≥ (a) − 2.

**Rủi ro.** Bộ lọc có thể loại quá nhiều. Nếu dưới 1 tham chiếu mỗi ảnh qua được, phải nới τ. Một rủi ro khác là cấu hình (c) nhảy định dạng mà không học được liên hệ kiểm kê → caption, đúng như VideoCap-R1 đã thấy với SFT. Khi đó cần thêm một vòng GRPO ngắn, vượt ngân sách 3 giờ.

### I4. Trục thứ ba: mức gọi tên ("Know, Mention, and *Name*")

**Luận điểm.** Ngoài hai trục *tồn tại* và *đáng nhắc*, còn trục **gọi tên ở mức nào**: hypernym chung ("người bán hàng", "chiếc xe") hay tên cấp nhập môn kiểu Việt ("gánh hàng rong", "xe ba gác", "nón lá"). Matcher đối tượng và CIDEr đều phạt khi mô hình đúng thực thể nhưng sai mức tên. Phần đáng kể của mức FP và FN hiện nay có thể là **sai mức tên** chứ không phải ảo giác hay lệch độ nổi bật. Đây là giả thuyết, chưa đo.

**Vì sao chưa ai làm.** Entry-level naming (Ordonez, ICCV 2013) có từ trước thời VLM và chỉ cho tiếng Anh. MELLA xử lý thực thể văn hóa bằng dữ liệu alt-text, nhưng không đo mức tên và không gắn với metric tham chiếu. Chưa ai phân rã lỗi caption thành ba lớp: ảo giác, độ nổi bật và mức tên.

**Cơ chế.**
1. Khai thác từ tham chiếu KTVIC train các cặp (tên chung → tên đặc thù) cùng chỉ một đối tượng trong cùng ảnh, từ caption của các người gán khác nhau.
2. Ước lượng P(tên đặc thù | thực thể, ảnh) bằng đồng thuận giữa người gán.
3. Kiểm chứng tên đặc thù bằng probe hoặc verifier. Một tên đặc thù sai thì là ảo giác *nặng hơn*.
4. Nâng mức tên trong mục tiêu SFT chỉ khi đã được kiểm chứng.

**Thí nghiệm đầu, khoảng 0,5 GPU-giờ, chủ yếu CPU.**
1. Trên dev, đếm tỷ lệ FP và FN của zero-shot và VSPS có thể giải thích bằng "đúng hypernym, sai mức", qua bảng ánh xạ khai thác ở bước 1 của cơ chế.
2. Thay tên trong caption theo kiểu oracle để đo trần CIDEr và F1.

Bác bỏ nếu dưới 10% lỗi đối tượng thuộc lớp sai mức tên, hoặc nếu trần CIDEr tăng dưới 3 điểm.

**Rủi ro.** KTVIC có thể ít thực thể đặc thù văn hóa, vì đây là miền đời sống chung. Bảng ánh xạ tự động có thể nhiễu. Ngoài ra cần gold-300 để chứng minh tên đặc thù là *đúng* chứ không chỉ khớp tham chiếu.

## 4. Quan hệ với Know-and-Mention (05_TONG_HOP_XEP_HANG.md)

| Ý tưởng | Quan hệ | Cụ thể |
|---|---|---|
| I1 Plural-Optimal | **Bổ sung, là tầng quyết định của KaM** | KaM dùng P(tồn tại) × P(đáng nhắc) với một ngưỡng chỉnh trên dev, tức là heuristic. I1 thay ngưỡng đó bằng quyết định tối ưu F1 kỳ vọng theo từng ảnh, và cho KaM một phát biểu hình thức: đánh đổi xuất hiện vì ngưỡng cố định. Nên gộp I1 vào KaM thành đóng góp lý thuyết. |
| I2 Classifier Checkpoints | **Trực giao** | KaM làm việc ở khâu dữ liệu và SFT, còn I2 làm ở khâu giải mã. Probe tồn tại của KaM có thể dùng trực tiếp làm bộ chấm tại loại từ. Nên coi I2 là thí nghiệm phụ hoặc một bài riêng về ngôn ngữ học. |
| I3 Inventory-then-Select | **Cạnh tranh một phần** | Cả hai đều dựng mục tiêu SFT. KaM render template từ tập đã chọn, nên vẫn mang rủi ro CIDEr thấp của VSPS. I3 giữ văn phong người. Có thể kết hợp: dùng điểm KaM làm τ cho bộ lọc của I3. Nếu I3 thắng về CIDEr, nó nên là *đầu ra* của KaM thay cho template. |
| I4 Know-Mention-Name | **Bổ sung, mở rộng thành 3 trục** | Phép phân rã của KaM (i)–(iv) thêm lớp (v): "đúng thực thể, sai mức tên". I4 tăng sức nặng cho con số tiêu đề "bao nhiêu phần của sự đánh đổi không phải ảo giác", và là góc văn hóa và ngôn ngữ mà reviewer Q1 thường đòi ở bài về ngôn ngữ ít tài nguyên. |

**Khuyến nghị thứ tự:** I1 và I4, chủ yếu chạy CPU, nên chạy ngay cùng phép đo không cần gold của KaM. Sau đó chạy I3, phần quyết định về CIDEr. I2 chỉ nên làm sau khi có số liệu độ phủ loại từ đo bằng POS thật.

**Ghi chú xác minh:** Các link arXiv và venue trong mục 1 đã được kiểm qua tìm kiếm ngày 11/10/2026, trừ những mục ghi UNVERIFIED. Bài GFM của Dembczyński (NeurIPS 2011) được trích theo trí nhớ, **phải kiểm link trước khi dùng**. Số đếm loại từ là thống kê thô do tôi tự đếm trên `data/datasets/ktvic/train_data.json`.
