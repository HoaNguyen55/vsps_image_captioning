# Tổng hợp kiểm tra trùng lặp nội dung nghiên cứu (10 agent, 2026-10-10)

Nguồn chi tiết: `01_…` đến `10_…` trong thư mục này. Mỗi bài trong đó đều có DOI hoặc arXiv đã được agent mở ra kiểm, hoặc đối chiếu qua OpenAlex/Crossref. Bài nào chưa xác minh được thì có ghi rõ ở cuối từng file.

## 1. Kết luận

- **Không có bài nào trùng toàn bộ phương pháp VSPS.** Cả 10 hướng tìm kiếm đều đi tới cùng một kết luận. Chưa có công trình nào kết hợp đủ 4 thành phần:
  1. dùng mệnh đề có kiểu đã kiểm chứng để **dựng** target SFT, không dùng gold caption;
  2. verdict 3 trạng thái, tạo từ cặp truy vấn khẳng định + phủ định lấy mẫu K lần;
  3. trung hòa phần không chắc thay vì xóa bỏ;
  4. render có truy vết span ← mệnh đề ← verdict.
- **Nhưng hầu hết từng thành phần riêng lẻ đều đã có tiền lệ.** Bài phải bảo vệ tính mới ở **tổ hợp và cơ chế**, không được khẳng định từng phần là mới. Hiện bản v9 viết đóng góp (1) và (2) quá rộng.
- **Bài journal nào trùng ở mức HIGH?** Không có (agent 10 rà khoảng 90 truy vấn trên OpenAlex/Crossref). Các bài trùng HIGH đều là bài hội nghị lớn, xem mục 2.

## 2. Bài BẮT BUỘC thêm vào và đối chiếu (bản v9 chưa trích dẫn)

| Bài | Nơi đăng | Trùng với | Điểm khác biệt VSPS cần nói rõ |
|---|---|---|---|
| **HalluciDoctor** | CVPR 2024, DOI 10.1109/CVPR52733.2024.01230 | **C1 HIGH**, C2 medium | Bài đó dùng nhiều MLLM kiểm chéo rồi **xóa** span lỗi khỏi văn bản có sẵn, verdict nhị phân. VSPS **dựng** target từ mệnh đề, không dùng gold, có 3 trạng thái và trung hòa |
| **Image Textualization** | NeurIPS 2024 D&B (agent 02 chưa xác minh được venue; nếu chưa chắc thì trích arXiv 2406.07502) | **C1 HIGH** | Bài đó chỉ kiểm object bằng detector, nhị phân, rồi để LLM viết lại tự do. VSPS có mệnh đề có kiểu, xử lý UNCERTAIN, và render truy vết được |
| **RLAIF-V** | CVPR 2025, DOI 10.1109/CVPR52734.2025.01861 | C1, C2 medium | Cùng chuỗi claim → câu hỏi có/không → dữ liệu, nhưng bài đó dùng DPO và verdict nhị phân. Phản biện dễ hỏi "VSPS = RLAIF-V + SFT?". Trả lời bằng 3 trạng thái, trung hòa, dựng target, và kết quả DPO thất bại ở §IV-E9 |
| **SENTINEL** | ICCV 2025, DOI 10.1109/ICCV51701.2025.00067 | **C2 medium-high** | Bài đó **đã có** nhãn hallucinated / factual / uncertain (do 2 detector bất đồng) và bỏ phần uncertain. Vì vậy "3 trạng thái" không còn là mới. Tính mới phải đặt ở *nguồn* của bất định (cặp khẳng định/phủ định lấy mẫu, áp cho mọi loại mệnh đề) và *cách dùng* nó (trung hòa) |
| **Visual Fact Checker** | CVPR 2024 | C1, C4 medium | Bài đó verify rồi viết lại caption **lúc suy luận** |
| **Women also Snowboard / Equalizer** | ECCV 2018 | **C3 medium-high** | Nguồn gốc kinh điển của ý tưởng "nói *person* khi bằng chứng về giới yếu". VSPS khác ở cơ chế: chọn lọc, có verifier gác, offline, ở mức dữ liệu |
| **LIBRA** | CVPR 2023 (+ IEICE 2025) | C3 medium | Bài đó sửa từ giới tính **sau khi sinh** bằng một bộ editor đã học |
| **BioPro** | ACM MM 2026, arXiv 2512.00807 | C3, C5 medium | Cùng mục tiêu "trung tính khi không chắc", nhưng làm lúc suy luận và cần nhãn giới tính do người gán |
| **Conformal Linguistic Calibration** | NeurIPS 2025 | **C3 HIGH (về nguyên lý)** | Cùng nguyên lý "giảm độ cụ thể của claim không chắc rồi huấn luyện trên bản viết lại", nhưng chỉ cho văn bản. VSPS làm cho ảnh, cắt bỏ một thành phần theo cách tất định, dựa trên bằng chứng thị giác đã lưu |
| **HQM "Measuring the Measurers"**; **UHP Detection** | arXiv 2406.17115; arXiv 2608.03817 | C2 medium | Cặp câu hỏi khẳng định/phủ định để phát hiện acquiescence **đã có**. VSPS chỉ được nhận là người biến nó thành luật quyết định cho từng mệnh đề trong pipeline dữ liệu |
| **SelfCheckGPT**; **VL-Uncertainty** | EMNLP 2023; arXiv 2411.11919 | C2 medium | Dùng mức đồng thuận giữa các mẫu làm tín hiệu. VL-Uncertainty còn chỉ ra các mẫu có thể đồng thuận mà vẫn sai: đây là phản biện sẵn cho ngưỡng 5/5. Trả lời bằng audit người ở §IV-E7 |
| **HSA-DPO**, **CCCaption** (đã trích), **ClaimDiff-RL**, **OSCAR** (IJCAI 2026), **SEED** (ACM MM 2025) | — | C1 medium | Biến verification thành tín hiệu huấn luyện qua cặp preference hoặc reward. SEED dùng **đúng** lập luận "lọc offline rồi chưng cất vào mô hình một lượt", nên "single-pass" không được coi là một đóng góp |
| **HELTA** | IEEE T-ITS 2025, DOI 10.1109/TITS.2025.3625700 | C1 medium | Dữ liệu mô tả "không ảo giác" làm offline bằng kiểm chéo entity nhị phân |
| **AQAH** | IEEE TCSVT 2025, DOI 10.1109/TCSVT.2025.3618949 | C2 medium | Dùng bất đồng giữa các mẫu để tìm phần không chắc, nhưng hỏi lại lúc suy luận |
| **MHR (Qu et al.)** | ACM TOMM 2026, DOI 10.1145/3797025 | C1, C5 medium | Tự nhận là "first attempt" về ảo giác LVLM ngoài tiếng Anh (13 ngôn ngữ, không có tiếng Việt) |
| **AutoViVQA** | Springer CCIS 2026, DOI 10.1007/978-981-92-0068-9_33 | C1 medium (tiếng Việt) | Lọc dữ liệu VQA tiếng Việt bằng bỏ phiếu đa số: giữ hoặc bỏ cả mẫu, không xét từng mệnh đề |
| **EPAlign** | IEEE TASLP 2026 | ủng hộ động cơ C1 | Dữ liệu chi tiết hơn khả năng nhận thức của mô hình gây ra ảo giác |
| **FaithScore**, **DSG** | EMNLP-F 2024; ICLR 2024 | **C4** | 5 loại mệnh đề cơ bản là atomic fact có kiểu của hai bài này. Trình bày là *kế thừa*; phần mới là truy vết từng span |

KnowAda [12], CapMAS / Lee et al. [10], Woodpecker [15] và CCCaption [18] đã được trích. Cần giữ và làm rõ hơn phần đối chiếu với các bài này.
Nên trích thêm (mức thấp đến trung bình): ConfLVLM (EMNLP 2025), HallE-Control, LURE [14], MELLA (IJCAI 2026, có tiếng Việt nhưng dữ liệu dịch máy, không kiểm chứng), ViG (IEEE MAPR 2026, baseline KTVIC mới, phản biện có thể đòi so sánh), LOTUS (ACL 2025), Med-StepBench (IJCAI 2026), ViHallu (arXiv 2026), DCScore/FeedQuill (ICLR 2025), EDC (CVPR 2026).

## 3. Khẳng định trong bài phải THU HẸP hoặc BỎ

| Khẳng định hiện tại / ngầm định | Vấn đề | Cách viết an toàn |
|---|---|---|
| Đóng góp (1): "verification điều khiển chất lượng dữ liệu thay vì sửa đầu ra" | HalluciDoctor, Image Textualization, KnowAda, HELTA đã làm ở mức dữ liệu | "**dựng** target SFT trực tiếp từ mệnh đề có kiểu đã kiểm chứng (không gold, không xóa trên văn bản có sẵn), mỗi span truy vết được" |
| Đóng góp (2): "thiết kế 3 trạng thái" | SENTINEL đã có 3 nhãn; cặp phủ định (HQM) và đồng thuận mẫu (SelfCheckGPT) đã có | "verdict 3 trạng thái **cho mọi loại mệnh đề**, sinh từ cặp truy vấn khẳng định/phủ định K = 5 lần; acquiescence → UNCERTAIN; luật trần chỉ hạ mức; **và dùng UNCERTAIN để trung hòa thay vì loại bỏ**" |
| Single-pass là ưu điểm | SEED, RLAIF-V, các phương pháp DPO đều single-pass | Chỉ nêu như một tính chất, không gọi là đóng góp |
| Trung hòa giới tính | Burns 2018, LIBRA, BioPro, CLC | "trung hòa **chọn lọc, offline, trong dữ liệu**, do verifier gác, áp cho danh từ chỉ người mang giới trong tiếng Việt; giới tính đã kiểm chứng thì giữ lại" |
| "Đầu tiên" | Med-StepBench (y khoa, Việt/Anh), MHR (đa ngôn ngữ) | "**theo hiểu biết của chúng tôi**, là công trình đầu tiên đo và giảm ảo giác object và giới tính trong **mô tả ảnh chi tiết tiếng Việt, miền tổng quát**" |
| 5 loại mệnh đề | FaithScore, DSG | "theo cách biểu diễn atomic fact có kiểu của [FaithScore, DSG]" |

Các khoảng trống vẫn có thể nhận là của VSPS (nhiều agent cùng xác nhận):
- chưa có CHAIR hay POPE tiếng Việt;
- chưa có lexicon object tiếng Việt;
- chưa có metric ảo giác giới tính cho caption tiếng Việt;
- chưa có công trình về "xanh" (lam/lục);
- chưa có dữ liệu giám sát tiếng Việt đã kiểm chứng cho captioning.

## 4. Câu khẳng định tính mới đề xuất (gộp từ 10 hướng)

> Prior data-centric methods clean SFT data by deleting spans that fail a binary consistency or detector check (HalluciDoctor, Image Textualization, HELTA) or by adapting captions to the student model's knowledge (KnowAda), while preference- and reward-based methods (RLAIF-V, HSA-DPO, CCCaption) turn claim-level verification into ranked pairs or scalar rewards. VSPS instead *constructs* each SFT target from typed atomic propositions (following FaithScore/DSG) that carry a three-state verdict obtained from paired affirmative and negated queries sampled K times, where a split vote or acquiescence yields UNCERTAIN. Refuted content is dropped, and under-evidenced content is neutralized to its still-verifiable part, rather than discarded (cf. SENTINEL) or penalized; in Vietnamese this selectively removes unsupported gender from person nouns while keeping verified gender (cf. Burns et al.; LIBRA). Every rendered span traces back to its proposition and verdict, and training uses the standard SFT loss. To our knowledge, this is also the first measurement and reduction of object and gender hallucination in general-domain detailed Vietnamese captioning.

## 5. Việc còn phải làm trước khi nộp

1. Đọc toàn văn (không chỉ abstract) của **HalluciDoctor, Image Textualization, SENTINEL, RLAIF-V, Conformal Linguistic Calibration, BioPro, SEED, OSCAR**, rồi viết đoạn đối chiếu dài 1–2 câu cho từng bài trong Related Work.
2. Kiểm lại trên IEEE Xplore: 6 bài journal mà agent 10 chỉ đánh giá được qua tiêu đề (trong đó có REVERIE+, IJCV 2026), và xem HalluciDoctor, RLAIF-V, HALVA, KnowAda đã có bản journal chưa.
3. Xác minh các mục "unverified": venue của Image Textualization; Vistral-V (LNNS 2026); HDUCap (JVCIR 2026); tác giả của PALO và GAIC; HalDec-Bench v2 (đã bị rút trên arXiv, không trích).
4. Cập nhật trích dẫn: UIT-OpenViIC → SPIC 140 (2026) 117430; ReflectCAP [11] → Springer LNCS; thêm DOI cho Woodpecker [15].
5. Cân nhắc thêm baseline ViG (KTVIC), RLAIF-V-7B và HalluciDoctor (nếu có code) cho bản journal.
6. Chạy phần mềm kiểm tra trùng lặp văn bản (iThenticate/Turnitin) cho bản thảo. Báo cáo này chỉ đánh giá trùng lặp **ý tưởng và nội dung nghiên cứu**, không kiểm câu chữ.
