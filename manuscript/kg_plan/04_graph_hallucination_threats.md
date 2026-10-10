# 04. Đồ thị để giảm ảo giác và kiểm chứng đầu ra LVLM/MLLM (2025-2026): bản đồ và "threat papers"

Agent 04, ngày 2026-10-10. Góc nhìn: scene graph, KG, đồ thị thực thể/quan hệ dùng để **giảm ảo giác hoặc kiểm chứng** caption/VQA. Gồm: graph-based verification, KG fact-checking, graph-guided decoding, dữ liệu preference/RL có cấu trúc đồ thị, ảo giác quan hệ, xung đột tri thức (parametric và KG), và grounding tri thức văn hóa (Việt Nam, châu Á).

**Cách xác minh.** arXiv export API trả 429, OpenAlex hết quota ngày (429), Semantic Scholar 429. Vì vậy mọi bài dưới đây đều được **mở trực tiếp trang `arxiv.org/abs/<id>`**: đọc tiêu đề, ngày, comment (venue) và abstract. Riêng AKGMA được tra qua Crossref DOI. Bài được tìm bằng `arxiv.org/search` (searchtype=abstract) với khoảng 40 truy vấn. Venue chỉ ghi khi trường comment của arXiv hoặc Crossref có nêu. Kết quả là con số trong abstract; abstract không có số thì ghi "không nêu số". Cột code ghi link có trong abstract hoặc comment; "–" nghĩa là abstract không có link (không có nghĩa là không có code).

---

## 1. Bức tranh: đồ thị vào ở đâu

| Vai trò của đồ thị | Mức độ đông đúc 2025-2026 | Bài đại diện |
|---|---|---|
| (V) **Kiểm chứng/sửa hậu kỳ**: đồ thị là "visual KB" để phát hiện hoặc viết lại | Trung bình, chủ yếu arXiv | CutPaste&Find, RelCheck, Multi-hop KG verify |
| (P) **Dữ liệu preference/RL dựng từ đồ thị** (hard negative từ nhiễu nút SG, reward theo tập object/attr/rel) | **Tăng nhanh**, có ICCV/EMNLP | SceneAlign, SC-Captioner, FoCUS, CheXPO-v2 |
| (D) **Giải mã/attention cho ảo giác quan hệ** (thường không có đồ thị tường minh, chỉ có cấu trúc subject-relation-object) | Đông, có ICLR | ChainMPQ, IVE, RVE, constraint-aware prompting |
| (B) **Benchmark ảo giác dựa trên triple/SG/tri thức** | Đông | Tri-HE, Reefknot, KnowHal, M²CQA |
| (K) **KG ngoài làm ngữ cảnh/căn chỉnh, và xung đột tri thức** | Tăng, có AAAI/CVPR/ICCV | AKGMA, KG-ViP, GraphLoom, MMGraphRAG, VaLiK, CC-VQA |
| (C) **Grounding tri thức văn hóa** (KG/Wikipedia → dữ liệu hoặc RAG) | Tăng, có ICLR/ACL | CulturalGround, RAVENEA, SEA-VL, VietMEAgent |

Nhận xét chính: hầu hết bài (V), (P) và (B) dùng **scene graph tiếng Anh dựng từ Visual Genome/COCO hoặc từ parser tiếng Anh**. Nhánh (C) dùng **Wikidata/Wikipedia** ở cấp thực thể nổi tiếng. **Chưa thấy bài nào** dùng đồ thị *đã kiểm chứng trên ảnh* để tạo dữ liệu huấn luyện caption **tiếng Việt**. Kết luận này dựa trên các truy vấn `Vietnamese multimodal hallucination`, `Vietnamese knowledge graph` và `Vietnamese image captioning` trên arXiv: không có kết quả nào thuộc nhóm hallucination/KG-captioning.

---

## 2. Danh mục bài (đã mở trang abs)

### 2.1 (V) Kiểm chứng và sửa bằng đồ thị
| Bài | Venue | Đồ thị vào ở đâu | Phương pháp | Kết quả (theo abstract) | Code |
|---|---|---|---|---|---|
| **CutPaste&Find** (Nguyen C.-D. et al.), arXiv 2502.12591 | không ghi | "Visual-aid Knowledge Base" mã hóa quan hệ entity-attribute kèm ảnh | Phát hiện ảo giác không cần huấn luyện và không gọi LVLM, dùng mô-đun thị giác/ngôn ngữ có sẵn, có scaling factor cho similarity | Cạnh tranh trên POPE và R-Bench, rẻ hơn nhiều | – |
| **RelCheck** (Patil et al.), arXiv 2609.27890 | không ghi | KB 3 lớp: triple SG (RelTR), vị từ không gian từ bbox, claim object kiểu Woodpecker | LLM corrector viết lại câu ảo giác, hậu kỳ, không huấn luyện | LLaVA v1 13B: MME hallucination 630,0 so với 585,0 (Woodpecker-style). Position: acc+ từ 0,367 lên 0,600. Ablation McNemar p=0,025 | – |
| **Beyond Generation: Multi-Hop Reasoning** (Hossain), arXiv 2511.20531 | NewInML workshop @ICML 2025 | Duyệt KG nhiều bước: nhận dạng thực thể → traversal → sửa caption | So sánh biểu diễn tri thức dạng phân cấp, triple và bullet | Factual accuracy tăng khoảng 31% trên tập tự curate nhỏ (Landmarks v2 + CC + COCO), "preliminary" | – |
| **Bottom-Up Holistic Reasoning** (Wu S. et al.), arXiv 2412.11124 (nền, 12/2024) | AAAI 2025 | Scene graph biểu diễn ảnh, cộng commonsense cho tầng cognition | Kiểm chứng và tích hợp từ perception lên cognition, xử lý cả input văn bản sai | "Cải thiện đáng kể" trên nhiều benchmark, không nêu số | – |

### 2.2 (P) Preference/RL có cấu trúc đồ thị
| Bài | Venue | Đồ thị vào ở đâu | Phương pháp | Kết quả | Code |
|---|---|---|---|---|---|
| **SceneAlign** (Wang C. et al.), arXiv 2601.05600 | Preprint | Xác định **nút SG quan trọng cho suy luận**, nhiễu bằng 4 chiến lược mô phỏng lỗi grounding | Hard-negative rationale (hợp lý về ngôn ngữ nhưng sai về thị giác) → **DPO** | Cải thiện accuracy và faithfulness trên 7 benchmark suy luận thị giác, không nêu số | – |
| **SC-Captioner** (Zhang L. et al.), arXiv 2508.06125 | **ICCV 2025** | Parse caption dự đoán và caption tham chiếu thành tập object/attribute/relation | RL self-correction. Reward = bonus cho phần thêm/bớt đúng, phạt phần sai, đo theo hiệu tập. Metric cải tiến từ CAPTURE. Dataset RefinedCaps 6,5K ảnh COCO | Vượt DPO "đáng kể" | – |
| **FoCUS** (Hyun et al.), arXiv 2609.00709 | **EMNLP 2026 Main** | Caption được căn chỉnh với thành phần SG (object/attr/rel), có trọng số (cả âm) theo prompt điều khiển | GRPO + ngưỡng object validity chặt + verification bằng suy luận cho attr/rel. Benchmark SCoPE (Include/Avoid) | Cải thiện controllability và chất lượng chi tiết trên 2 backbone, không giảm caption chung | https://focus-emnlp2026.github.io/ |
| **CheXPO-v2** (Liang et al.), arXiv 2512.17213 | Preprint (y tế) | Parse bước suy luận thành triple (Disease, Relation, Anatomy) → **KG Consistency Reward** | GRPO, process supervision, hard-example mining | SOTA trên MIMIC-CXR-VQA với 5k mẫu | https://github.com/ecoxial2007/CheX-Phi4MM |
| **ClaimDiff-RL** (Li T. et al.), arXiv 2605.20278 | Preprint | Không phải đồ thị mà là claim nguyên tử có kiểu (họ hàng gần) | Reward = khác biệt claim so với caption tham chiếu, đã kiểm trên ảnh, có loại lỗi và mức độ | Cân bằng ảo giác và thiếu sót tốt hơn. Vượt Gemini-3-Pro-Preview ở một số chiều (đếm, quan hệ không gian) | – |
| **HII-DPO** (Yang Y. et al.), arXiv 2602.10425 | Preprint | Prior đồng xuất hiện theo cảnh (ngầm, không phải SG tường minh) | Xóa object trong ảnh → ảnh gây ảo giác → cặp preference. Benchmark MOH | Tốt hơn SOTA tới 38% trên benchmark ảo giác chuẩn | – |

### 2.3 (D) Giảm ảo giác quan hệ khi giải mã hoặc prompting
| Bài | Venue | Cấu trúc dùng | Phương pháp | Kết quả | Code |
|---|---|---|---|---|---|
| **ChainMPQ** (Wu Y. et al.), arXiv 2510.06292 | **ICLR 2026** | Tách subject / object / relation thành câu hỏi đa góc nhìn | Chuỗi xen kẽ ảnh và văn bản có bộ nhớ, không huấn luyện | "Giảm đáng kể" ảo giác quan hệ trên nhiều LVLM | – |
| **IVE: Attention at Rest Stays at Rest** (Gong et al.), arXiv 2604.01989 | không ghi | Không có đồ thị. Phát hiện "visual inertia" khi sinh token quan hệ | Hiệu chỉnh visual value theo lịch sử attention | Giảm ảo giác quan hệ trên 3 MLLM, không nêu số | – |
| **RVE** (Qin Z. et al.), arXiv 2605.11808 | không ghi | Không có đồ thị. Điểm ARS chọn head nhạy với quan hệ hành động | Tăng attention vào vùng liên quan hành động | Vượt baseline, chi phí không đáng kể, tổng quát sang quan hệ không gian và object | – |
| **Constraint-Aware Prompting** (Wu J. et al.), arXiv 2502.08317 | không ghi | Ràng buộc 2 chiều và bắc cầu trên quan hệ không gian (logic đồ thị) | Prompting | Cải thiện trên 3 tập quan hệ không gian | – |
| **When Relations Break** (Shin et al.), arXiv 2605.05045 | không ghi | Phân tích | Xoay ảnh và thêm nhiễu làm hỏng suy luận quan hệ | Chỉ có phát hiện định tính | – |

### 2.4 (B) Benchmark dựa trên triple, SG hoặc tri thức
| Bài | Venue | Ghi chú | Code/data |
|---|---|---|---|
| **Tri-HE** (Wu J. et al.), arXiv 2410.23114 (nền) | **TMLR 2025** | Đánh giá ảo giác qua triple (obj, rel, obj) trích từ câu trả lời. Ảo giác quan hệ nặng hơn ảo giác object. Kèm cách giảm không huấn luyện | https://github.com/wujunjie1998/Tri-HE |
| **Reefknot** (Zheng K. et al.), arXiv 2408.09429 | **Findings ACL 2025** | Hơn 20.000 mẫu dựng từ SG Visual Genome. Giảm ảo giác dựa trên confidence: −9,75% trung bình trên 3 tập | – |
| **KnowHal** (Li R. et al.), arXiv 2608.03782 | Preprint | 1.800 mẫu, 4 chiều (entity/attr/relation/**knowledge**), cặp câu hỏi dương/âm, 14 MLLM. Chiều knowledge khó nhất | – |
| **M²CQA / CFHR** (Mousi et al.), arXiv 2602.05437 | (file 00 ghi Findings ACL 2026, chưa đối chiếu) | Ảo giác **phản thực tế hợp lý về văn hóa**, 17 nước MENA, tiếng Anh, tiếng Ả Rập và phương ngữ. CFHR tăng mạnh ở phương ngữ. Reasoning-first làm ảo giác tăng | https://huggingface.co/datasets/QCRI/M2CQA |
| **PancapChain / PancapScore** (Lin K.-Y. et al.), arXiv 2505.16334 | **NeurIPS 2025** | Caption "panoptic" (entity, vị trí, thuộc tính, quan hệ). PancapChain-13B vượt InternVL-2.5-78B | https://visual-ai.github.io/pancap/ |

### 2.5 (K) KG ngoài, đồ thị lai, xung đột tri thức
| Bài | Venue | Đồ thị vào ở đâu | Phương pháp | Kết quả | Code |
|---|---|---|---|---|---|
| **AKGMA** (G. Li, Hu, Li, Yao, Mi), DOI 10.1609/aaai.v40i18.38532 | **AAAI 2026** (Crossref) | EKA nối visual entity với KG cho một LM nhỏ. AKGC dùng **RL dựng subgraph liên quan ảnh** để "improve knowledge hallucinations". SCKA lấy **scene graph annotation** bơm vào LLM | Captioning LMM tăng cường tri thức, dataset **UniKnowCap** (knowledge accuracy + detail consistency) | "Outperforms baselines across multiple metrics", abstract không nêu số | – |
| **KG-ViP** (Li Z. et al.), arXiv 2601.11632 | ACL 2026 theo S2 (file 11, chưa đối chiếu) | Hợp nhất **scene graph** (chi tiết thị giác) với **commonsense graph** (tri thức), truy hồi theo câu hỏi | Retrieval-and-fusion → ngữ cảnh có cấu trúc | Vượt các phương pháp VQA trên FVQA 2.0+ và MVQA, không nêu số | – |
| **GraphLoom** (Ali et al.), arXiv 2608.15056 | Preprint | MMKG cấp instance gồm mô tả cảnh grounded, triple và commonsense | Truy hồi subgraph có hiệu chỉnh độ tin cậy, graph memory slot vào LM đóng băng | ScienceQA, MultiModalQA, OK-VQA (có distractor) | – |
| **MMGraphRAG** (Wan, Yu), arXiv 2507.20804 | Preprint | Ảnh → scene graph, liên kết với KG văn bản (SpecLink, spectral clustering) | GraphRAG đa phương thức. Dataset CMEL | Tốt hơn trên DocBench và MMLongBench | – |
| **VaLiK** (Liu J. et al.), arXiv 2503.12972 | **ICCV 2025** | Dựng MMKG không cần nhãn bằng chuỗi VLM và lọc bằng similarity | Tăng cường suy luận cho LLM | Vượt SOTA trên các tác vụ suy luận đa phương thức | https://github.com/Wings-Of-Disaster/VaLiK |
| **VisKG** (Chen T.-C. et al.), arXiv 2609.35942 | Preprint | RL học dịch ảnh thành **KG theo câu hỏi** (tối thiểu đủ) | GDPO + SFT có negative rationale | Abstract cắt trước phần số | – |
| **CC-VQA** (Hong Y. et al.), arXiv 2602.23952 | **CVPR 2026** | Không phải đồ thị. **Xung đột tri thức** giữa tri thức parametric và tri thức truy hồi, phân tích xung đột lấy thị giác làm trung tâm | Không huấn luyện, nén positional encoding, giải mã có trọng số theo xung đột | +3,3 đến +6,4% accuracy (E-VQA, InfoSeek, OK-VQA) | https://github.com/cqu-student/CC-VQA |
| **SegSub** (Carragher et al.), arXiv 2502.14908 | Preprint | Nhiễu ảnh có mục tiêu để tạo xung đột tri thức | Benchmark + fine-tune | Bám parametric 20%. Counterfactual <30%. Source conflict <1% | – |
| **Vision-Default, Prior-Override** (Lietzow et al.), arXiv 2606.28273 | Preprint | Cơ chế. 2,5-4,8% số head quyết định việc trả lời theo prior | Activation patching | Ablate các head này lật 68-96% câu trả lời từ prior sang thị giác | – |

### 2.6 (C) Tri thức văn hóa và địa phương
| Bài | Venue | Đồ thị/tri thức | Kết quả | Code/data |
|---|---|---|---|---|
| **CulturalGround / CulturalPangea** (Nyandwi, Song, Khanuja, Neubig), arXiv 2508.07414 | không ghi | **Wikidata KG** → ảnh thực thể văn hóa → 22M cặp VQA, 42 nước, 39 ngôn ngữ | +5,0 trung bình trên các benchmark văn hóa đa ngữ, không giảm tác vụ chính | – |
| **RAVENEA** (Li J. et al.), arXiv 2505.14462 | **ICLR 2026** | 11.396 tài liệu Wikipedia do người xếp hạng. Hai tác vụ: cVQA và **culture-informed image captioning (cIC)** | RAG văn hóa: +6% cVQA, **+11% cIC**. Hiệu quả dao động mạnh theo quốc gia | https://jiaangli.github.io/ravenea/ |
| **SEA-VL** (Cahyawijaya et al.), arXiv 2503.07920 | (file 00 ghi ACL 2025) | Dữ liệu, không có KG. 1,28M ảnh văn hóa Đông Nam Á, crawl đạt khoảng 85% liên quan văn hóa | – | HF SEACrowd collection |
| **VietMEAgent** (Nguyen H.-D. et al.), arXiv 2511.09058 | **FAIR 2025** (cùng hội nghị với VSPS) | **KB thực thể văn hóa Việt Nam** tự curate, detector đối tượng văn hóa, sinh chương trình. Dataset Vietnamese Cultural VQA (ẩm thực, kiến trúc, trang phục, lễ hội, nghệ thuật dân gian) | Abstract không nêu số | – |
| **Hierarchical Multi-Modal Retrieval for Knowledge-Grounded News Image Captioning** (Nguyen M.-L. et al.), arXiv 2606.18553 | SOICT 2025 | Truy hồi bài báo phân cấp → VLM mô tả → LLM ghép tri thức. Nhóm tác giả Việt, dữ liệu tin tức | Không nêu số trong phần đã đọc | – |
| **MERGE** (You X. et al.), arXiv 2511.21002 | **AAAI 2026** | KB đa phương thức hướng thực thể (EMKB) cho caption tin tức | CIDEr +6,84 (GoodNews), +1,16 (NYT800k). NER F1 +4,14 / +2,64. Visual News chưa thấy: CIDEr +20,17 | – |

---

## 3. Năm "threat papers" mạnh nhất với một "Vietnamese KG-grounded captioning transformer"

Giả định đề xuất mới có dạng: captioner transformer (hoặc LVLM QLoRA) + KG/scene graph + dữ liệu UIT, có nhắm vào ảo giác. Reviewer sẽ trích theo thứ tự sau.

### T1. AKGMA (AAAI 2026): "KG-guided captioning để giảm knowledge hallucination đã có ở hội nghị đỉnh"
- Vì sao nguy hiểm: trùng gần như cả ba từ khóa (KG + captioning + hallucination) và đã có KG subgraph dựng bằng RL, scene-graph adapter và dataset đánh giá riêng (UniKnowCap). Một kiến trúc "encoder + KG adapter + decoder" tiếng Việt sẽ bị coi là "AKGMA dịch sang tiếng Việt".
- Khác biệt bắt buộc: (a) đồ thị phải được **kiểm chứng trên từng ảnh** (trạng thái SUPPORTED/UNCERTAIN/REJECTED, như mệnh đề VSPS), không lấy từ annotation SG hay KG tĩnh. AKGMA dùng "scene graph annotations", còn tiếng Việt không có. (b) Phải đo **hai lỗi riêng biệt**: ảo giác thị giác (CHAIR/graph precision) và ảo giác tri thức (fact sai về thực thể). (c) Phải có **chính sách xung đột** tường minh (khi KG và ảnh mâu thuẫn thì thị giác thắng) kèm số liệu.

### T2. CulturalGround / CulturalPangea (arXiv 2508.07414; Neubig group): "grounding văn hóa bằng Wikidata cho 39 ngôn ngữ đã làm ở quy mô 22M"
- Vì sao nguy hiểm: phủ đúng luận điểm "cultural/local knowledge cho ngôn ngữ ít tài nguyên bằng KG". Reviewer sẽ hỏi vì sao không dùng CulturalPangea làm baseline.
- Khác biệt bắt buộc: (a) tác vụ là **caption chi tiết của cảnh đời thường**, không phải VQA về thực thể nổi tiếng. Thực thể UIT-OpenViIC/KTVIC (xe máy chở hàng, quán vỉa hè, nón lá) phần lớn **không có QID Wikidata riêng**, và cần một bảng đo độ phủ để chứng minh điều này (chưa đo). (b) Báo **CulturalPangea zero-shot** (nếu checkpoint công khai) trên cùng tập tiếng Việt. (c) Tri thức phải đi qua kiểm chứng ảnh trước khi vào caption, không chỉ làm dữ liệu huấn luyện.

### T3. RAVENEA (ICLR 2026): "culture-informed image captioning bằng truy hồi đã có benchmark và +11%"
- Vì sao nguy hiểm: đã có tác vụ cIC, đã cho thấy RAG văn hóa giúp caption, và đã ghi nhận hiệu quả khác nhau theo quốc gia.
- Khác biệt bắt buộc: (a) tri thức **có cấu trúc** (triple có kiểu, có trạng thái kiểm chứng) chứ không phải đoạn Wikipedia. Phải chứng minh đồ thị tốt hơn đoạn văn ở **cùng ngân sách token** (ablation đồ thị so với passage). (b) Phải đo **ảo giác do truy hồi gây ra**: caption thêm chi tiết đúng theo tài liệu nhưng không có trong ảnh. RAVENEA không tách lỗi này. (c) Dữ liệu và metric tiếng Việt.

### T4. KG-ViP (arXiv 2601.11632; ACL 2026 theo S2), cùng GraphLoom và Bottom-Up Holistic (AAAI 2025): "hợp nhất scene graph + commonsense graph để giảm knowledge hallucination"
- Vì sao nguy hiểm: ý "SG cho chi tiết thị giác + KG cho tri thức là bổ sung cho nhau" đã được viết rõ trong abstract. Một đề xuất "SG + ConceptNet" sẽ không còn mới.
- Khác biệt bắt buộc: (a) **sinh caption dài** (không phải VQA có câu hỏi làm cầu nối truy hồi). Truy hồi phải dựa trên đồ thị ảnh đã kiểm chứng, không dựa trên câu hỏi. (b) Dùng KG ở **phía kiểm chứng/trung tính hóa** (hard negative từ đồng xuất hiện, leo hypernym IsA cho mệnh đề UNCERTAIN, xem Ý 2 của file 11) thay vì chỉ làm ngữ cảnh đầu vào. (c) Báo chi phí suy luận một lượt, so với pipeline truy hồi nhiều bước.

### T5. Họ "đồ thị → preference/reward": SC-Captioner (ICCV 2025), FoCUS (EMNLP 2026), SceneAlign (2026)
- Vì sao nguy hiểm: nếu phương pháp mới huấn luyện bằng reward hay DPO dựa trên tập object/attr/rel của đồ thị, thì cả ba đều đã làm, và đều có GRPO/DPO trên LVLM. File 00 cũng đã ghi BalCapRL và ClaimDiff-RL cho reward theo claim.
- Khác biệt bắt buộc: (a) đồ thị tham chiếu **không cần caption hay SG chuẩn của người**: dựng từ mệnh đề đã kiểm chứng trên ảnh. SC-Captioner cần caption tham chiếu và RefinedCaps; FoCUS cần parse tiếng Anh. (b) **Trạng thái UNCERTAIN** sinh ra hành vi trung tính hóa, không chỉ thưởng/phạt nhị phân. (c) Có parser caption tiếng Việt → đồ thị và đánh giá độ chính xác của parser (tiếng Việt chưa có, xem file 11 mục 3.3).

### Bắt buộc trích thêm (không trong top 5 nhưng reviewer FAIR/Việt Nam sẽ nêu)
- **VietMEAgent (FAIR 2025)**: đây là KB văn hóa Việt Nam duy nhất đã thấy trong bối cảnh VLM, và cùng hội nghị. Cần nói rõ khác ở chỗ: VQA giải thích được dựa trên program, so với caption có kiểm chứng.
- **Tri-HE (TMLR 2025), Reefknot (Findings ACL 2025), ChainMPQ (ICLR 2026)**: nếu nói về "relation hallucination" thì phải trích, và nên dùng định nghĩa triple-level của Tri-HE cho metric tiếng Việt.
- **CC-VQA (CVPR 2026), SegSub, Vision-Default/Prior-Override**: nếu nói về xung đột giữa KG và ảnh.
- **RelCheck, CutPaste&Find**: baseline kiểm chứng hậu kỳ bằng đồ thị. Cả hai đều là arXiv và chạy trên model cũ (LLaVA v1 13B), nên là baseline rẻ dễ vượt.
- **M²CQA**: tiền lệ về "ảo giác văn hóa phản thực tế" ngoài tiếng Anh. CFHR có thể chuyển sang tiếng Việt.

---

## 4. Hàm ý cho kế hoạch KG (ngắn)
1. Đừng đặt đóng góp chính là "KG làm đầu vào cho bộ sinh" vì T1, T3 và T4 đã chiếm chỗ. Đóng góp nên là **đồ thị đã kiểm chứng trên ảnh** (đến từ VSPS) dùng cho (i) dữ liệu huấn luyện, (ii) metric graph P/R tiếng Việt kiểu Tri-HE/CompreCap, và (iii) KG ở phía kiểm chứng (hard negative, IsA neutralization).
2. Thí nghiệm tối thiểu để chống reviewer: tách ảo giác thị giác và ảo giác tri thức; ablation đồ thị so với passage ở cùng số token; có baseline CulturalPangea hoặc RAG kiểu RAVENEA trên ảnh tiếng Việt; báo độ phủ Wikidata/ConceptNet trên lexicon đối tượng UIT.
3. Ô trống còn lại (đã quét, không thấy bài): benchmark ảo giác quan hệ/tri thức tiếng Việt; dữ liệu preference dựng từ đồ thị cho caption tiếng Việt; metric đồ thị tiếng Việt.

## 5. Chưa xác minh / hạn chế
- Không truy cập được arXiv API, OpenAlex và Semantic Scholar hôm nay (429/quota). Tìm kiếm chỉ dùng `arxiv.org/search`, nên có thể sót bài chỉ có trên ACL Anthology/CVF hoặc chỉ có trong proceedings.
- Venue của KG-ViP (ACL 2026), M²CQA (Findings ACL 2026) và SEA-VL (ACL 2025) lấy từ file 11/00, chưa đối chiếu với proceedings. Comment arXiv của các bài này không ghi venue.
- CulturalGround có bao gồm tiếng Việt trong 39 ngôn ngữ hay không: **chưa kiểm**. Checkpoint CulturalPangea có công khai không: chưa kiểm.
- AKGMA: chỉ đọc abstract qua Crossref, chưa có số liệu, chưa thấy code.
- Cột "Code" chỉ phản ánh link trong abstract/comment, chưa tìm trên GitHub.
- Không tìm thấy bài 2025-2026 nào dựng **cặp DPO trực tiếp từ scene graph cho captioning** ngoài SceneAlign (suy luận/VQA) và SC-Captioner (RL, không phải DPO). Một tìm kiếm web cũng xác nhận là không thấy.
