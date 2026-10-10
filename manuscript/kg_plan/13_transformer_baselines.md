# 13. Captioner transformer không phải LVLM (2025-2026) và mô hình nhẹ cho ngôn ngữ ít tài nguyên: còn chỗ cho một captioner nhỏ có KG?

Ngày quét: 2026-10-10. Nguồn: Semantic Scholar Graph API (search/bulk, paper, citations), Crossref, PDF mở (arxiv.org/pdf, tạp chí HUFLIT, Hồng Đức, kho Huế). Hôm nay arXiv export API trả 429, OpenAlex hết quota và Elsevier/IEEE chặn, nên một số bài chỉ đọc được abstract. Số liệu nào chưa đọc được trong bảng gốc thì đưa xuống mục "Chưa xác minh".

**Trả lời ngắn.** Ngách này **còn, nhưng hẹp**, và chỉ đứng được nếu chơi đúng sân của nó: caption ngắn kiểu benchmark được chấm bằng metric tham chiếu (CIDEr). Trên sân này captioner nhỏ được huấn luyện có giám sát đang thắng LVLM zero-shot rất xa. Ví dụ: GRIT đạt CIDEr 136,0 trên KTVIC, trong khi Qwen2.5-VL-7B zero-shot trong repo này chỉ đạt 29,0 và VSPS đạt 17,3. Nhưng **chưa có bài nào so với LVLM đã fine-tune trên cùng train split tiếng Việt**, và đây là câu reviewer sẽ hỏi đầu tiên. Đối thủ gần nhất về ý tưởng là **ViG (MAPR 2026)**: GRIT đóng băng, thêm "relation memory" và "cultural query memory", vượt GRIT trên KTVIC và UIT-ViIC, và theo abstract còn vượt một mô hình đa phương thức lớn hơn đã fine-tune. Vì vậy một bài "GRIT + scene graph/ConceptNet cho tiếng Việt" sẽ nằm sát ViG, và chỉ đủ cho hội nghị khu vực (MAPR/RIVF/ACIIDS) hoặc tạp chí Q2-Q3, trừ khi có thêm một trục mới. Trục mới khả dĩ nhất là chưng cất đồ thị đã kiểm chứng của VSPS và đánh giá độ trung thực.

---

## 1. Bảng điểm cần vượt trên dữ liệu tiếng Việt (đã xác minh trong PDF/abstract)

Lưu ý so sánh: các bài khác nhau về tách từ (PyVI, RDRSegmenter hay âm tiết), split và cách scale (0-1 hay x100). Chỉ so trực tiếp các dòng cùng split chính thức.

### KTVIC (train 3.769 ảnh / test 558 ảnh, 5 caption/ảnh; caption đã tách từ sẵn)
| Hệ thống | Nguồn | B-1 | B-4 | METEOR | ROUGE-L | CIDEr | Ghi chú |
|---|---|---|---|---|---|---|---|
| ResNet101 + LSTM | KTVIC, arXiv 2401.08100, Bảng 3 | 53,0 | 15,5 | 27,5 | 42,3 | 21,8 | baseline gốc |
| ViT + Transformer | như trên | 56,1 | 19,3 | 30,1 | 44,7 | 36,8 | |
| **GRIT** | như trên | **74,7** | **40,6** | 36,6 | 59,7 | **136,0** | **mốc phải vượt**, code: github.com/davidnvq/grit/tree/vicap |
| Swin + Transformer decoder (pretrain COCO/Flickr30k, fine-tune KTVIC) | Tạp chí KH HUFLIT 2025, doi 10.71091/2354-113x/269, Bảng 1 | 65,2 | 21,5 | 26,9 | n/a | 58,5 | thấp hơn GRIT nhiều |
| ResNet101 + CLIP-text attention fusion | Tạp chí KH ĐH Hồng Đức số 84 (02/2026), doi 10.70117/hdujs.84.2.2026.1139, Bảng 2 | 66,7 | 26,6 | 22,9 | n/a | 84,1 | **tự chia lại 70/10/20**, không so được với split chính thức |
| ViG (GRIT đóng băng + Residual Relation Memory + Local-Cultural Query Memory) | MAPR 2026, doi 10.1109/MAPR72750.2026.11685699 | ? | ? | ? | ? | > 136,0 (theo abstract) | số cụ thể: Chưa xác minh |
| Qwen2.5-VL-7B zero-shot | repo, `data/results/zeroshot-short.json` (RDRSegmenter, word-level) | 30,7 | 5,5 | n/a | 25,6 | **29,0** | LVLM zero-shot. File ghi prompt "Mô tả chi tiết...", cần kiểm lại có đúng chế độ short không |
| VSPS (QLoRA SFT Qwen2.5-VL-7B), prompt short | repo, `data/results/main_s42-short.json` | 35,7 | 7,0 | 22,1 | 30,9 | **17,3** | |

### UIT-OpenViIC (ảnh đời sống Việt Nam). Số lấy từ arXiv 2305.04166, Bảng II-III, đặc trưng ResNeXt-152++ của VG
| Hệ thống | B-4 | METEOR | ROUGE-L | CIDEr |
|---|---|---|---|---|
| Transformer | 36,23 | 30,27 | 47,73 | 66,90 |
| AoANet | 36,65 | 30,72 | 48,36 | 69,42 |
| RSTNet | 36,77 | 30,71 | 48,96 | 72,72 |
| DIFNet | 37,67 | 30,90 | 49,13 | 74,19 |
| MDSANet | 38,80 | 31,05 | 49,77 | 75,58 |
| **MDSANet + CAMO** (đề xuất của bài) | **38,86** | 31,29 | 50,03 | **76,48** |

Cùng mô hình đạt khoảng 128-136 CIDEr trên COCO nhưng chỉ khoảng 67-76 trên OpenViIC, nên bộ này khó hơn hẳn. Bản tạp chí là Signal Processing: Image Communication, doi 10.1016/j.image.2025.117430 (Crossref ghi số tháng 01/2026). Chưa đọc được bản này, nên số có thể đã đổi.

### UIT-ViIC (3.850 ảnh COCO thể thao, 19.250 caption)
| Hệ thống | Nguồn | B-4 | ROUGE-L | CIDEr-D |
|---|---|---|---|---|
| pytorch-tutorial CNN-LSTM (PyVI) | arXiv 2002.00175, Bảng 3 | 39,4 | 62,6 | 100,5 |
| NIC Show-and-Tell (PyVI) | như trên, Bảng 4 | 32,7 | 59,9 | 81,8 |
| ResNet101 + CLIP-text attention fusion | Hồng Đức 2026, Bảng 1 (**tự chia 70/10/20**) | 27,8 | n/a | 87,4 |
| ViG | MAPR 2026 | ? | ? | > GRIT (theo abstract) |

Đáng chú ý: baseline năm 2020 trên split validation 924 ảnh đã đạt CIDEr-D 100,5, còn bài 2026 tự chia split lại báo con số thấp hơn. Nghĩa là trên UIT-ViIC chưa có một mốc chung đáng tin. Đây vừa là cơ hội (dựng lại baseline GRIT trên split chuẩn) vừa là rủi ro (reviewer hỏi split nào).

### Các bộ tiếng Việt khác (tham khảo)
- **ViTextCaps** (arXiv 2604.27712, 2026, scene-text), test set, tách âm tiết: PhonoSTFG CIDEr **64,6**, HSTFG 64,0, M4C 59,4, M2 Transformer (không copy) 2,6, người 80,8, **GPT-4o zero-shot 14,0** (METEOR cao nhất, 28,2). Bằng chứng trực tiếp: với metric tham chiếu, LMM zero-shot thua captioner chuyên biệt khoảng 4,6 lần.
- Flickr8k-Vi: DeepViT + ViT5 đạt B-4 37,98 (RIVF 2023, doi 10.1109/RIVF60135.2023.10471815; chỉ có abstract).
- sViIC: VisualRoBERTa (CNN + Transformer, pretrain trên 600K caption COCO dịch) B-4 66,85 (TALLIP 2024, doi 10.1145/3654796). sViIC không phải bộ UIT chính.
- Crossmodal-3600 (vi): VELVET (ConvNeXt V2 + BLOOMZ đóng băng) CIDEr 31,8 (FAIR 2025, doi 10.15625/vap.2025.0261).

**Mốc thực tế phải vượt:** KTVIC khoảng 136 CIDEr (GRIT), cao hơn nữa nếu lấy được số của ViG. OpenViIC 76,5. UIT-ViIC: tự dựng lại GRIT trên split chính thức.

---

## 2. Captioner transformer không phải LVLM, 2025-2026 (đã xác minh qua S2 hoặc PDF)

| Bài | Venue | Ý chính | Liên quan |
|---|---|---|---|
| ViG (H. T. Vu, N. H. Ngoc, T. C. P. Dinh, P. Do) | MAPR 2026 | Adapter gated-residual trên GRIT đóng băng: quan hệ cặp vùng (hình học + ngoại hình) và query "văn hóa Việt" học từ cụm từ khai thác trong caption | **Trùng lặp cao nhất** với ý "captioner nhỏ + quan hệ cho tiếng Việt" |
| Benchmarking Vietnamese image captioning: spatially-aware transformer + HDUCap (A. C. Hoang, H. L. Nguyen, T.-A. Pham, D. C. Nguyen) | J. Vis. Commun. Image Represent., 11/2026, doi 10.1016/j.jvcir.2026.104963 | Transformer có nhận biết không gian, kèm dataset mới HDUCap | Cho thấy captioner nhỏ tiếng Việt **vẫn lên được tạp chí Elsevier** năm 2026; số liệu: Chưa xác minh |
| Improving Efficiency Image Captioning by Attention + KG (T. K. Tran, N. T. U. Nhi, T. M. Le, N. T. Dinh) | ACIIDS 2025, LNAI 15684, doi 10.1007/978-981-96-6005-6_6 (đã đọc PDF) | Nhận diện đối tượng, dựng KG quan hệ, trộn với ConceptNet để sinh caption. Chỉ chạy trên **MS-COCO và Flickr30k**, chỉ báo BLEU-1/4 | Nhóm Việt đã làm "KG + ConceptNet captioning" bằng tiếng Anh. Trên dữ liệu UIT thì chưa có ai làm |
| Developing a Knowledge Graph for the Image Captioning Problem (cùng nhóm tác giả) | FAIR 2025, doi 10.15625/vap.2025.0297 | Không có abstract | Cùng hội nghị FAIR với VSPS. Cần đọc trước khi nộp |
| K-DFIC: Enriched Image Captioning Based on Knowledge Divergence and Focus (A.-A. Liu et al.) | IEEE TCSVT 2025 | Prompt nhận biết scene graph cho GPT-3.5 sinh "knowledge facts", rồi lọc và xếp lại cho decoder | Dạng KG/SG + transformer đã lên được Q1, nhưng dùng LLM ngoài |
| Knowledge-Driven Image Captioning (Haque et al.) | IEEE Access 2025, doi 10.1109/ACCESS.2025.3642465 | CapsNet + KG + Transformer decoder, COCO C 136,53 | Dòng "KG vào decoder" vẫn ra bài ở Q2-Q3 |
| Multi-step cross-attention + ConceptNet/TransE (L. Wang et al.) | Electronics 2025, doi 10.3390/electronics14163325 | CLIP-ViT + Faster R-CNN + BERT + GPT-2, tri thức ConceptNet nhiều bước | Tương tự |
| KG-augmented captioning, ViT-GAT (Mohapatra et al.) | AISP 2025 | ViT + ConceptNet qua GAT, Flickr30k B-4 0,38 / C 1,02 | Tương tự, venue nhỏ |
| I2OA: Intra- and Inter-Head Orthogonal Attention | IEEE TIP 2025 | Ràng buộc trực giao cho multi-head attention, không thêm tham số | Thủ thuật kiến trúc ghép được vào GRIT |
| ViPCap | AAAI 2025 | Prompt thị giác lấy từ văn bản truy hồi cho captioner nhẹ (họ SmallCap) | Baseline "lightweight + retrieval" cần trích |
| ClipCap++ | Applied Soft Computing 2025, doi 10.1016/j.asoc.2025.113469 | Tối ưu encoder ảnh + fine-tune LLM, họ CLIP-prefix | Không có abstract |
| Top-Down Semantic Refinement for Image Captioning | AAAI 2026 (S2), arXiv 2510.22391 | Chưa đọc | Chưa xác minh nội dung |

Ngôn ngữ ít tài nguyên, 2025-2026 (cùng mẫu "transformer nhỏ + đặc trưng ngữ nghĩa"): Assamese VSSA (TALLIP 2025, doi 10.1145/3717612; thuộc tính ngữ nghĩa + RL), AC-Lite Assamese (arXiv 2503.01453), Tamil DCAT (Applied Sciences 2025), Hindi ChitraVivran (TALLIP 2025), Urdu UICD (PLOS ONE 2025), Arabic BLIP-2 + CamelBERT (Applied Sciences 2026), shared task ImageEval 2025 tiếng Ả Rập (ArabicNLP 2025: 8 đội; system paper có region-aware transformer). Các bài này cho thấy TALLIP và tạp chí MDPI/PLOS vẫn nhận captioner nhỏ cho ngôn ngữ ít tài nguyên. Điều kiện là có dataset hoặc module mới, và hầu như **không có bài nào so với LVLM đã fine-tune**.

Trend scan ở 11 đã chỉ ra: SG/KG-làm-đầu-vào đạt đỉnh năm 2023. Truy vấn S2 `"image captioning" + "scene graph"` cho năm 2025-2026 chỉ ra 27 bài, và bài nhiều trích dẫn nhất (SC-Captioner, ICCV 2025) đã là LVLM + RL.

---

## 3. FEASIBILITY / OVERLAP / NOVELTY của "captioner transformer nhỏ + KG cho UIT"

**Feasibility: cao.** GRIT có sẵn nhánh `vicap` cho KTVIC. KTVIC chỉ có 3.769 ảnh train, nên huấn luyện cả XE lẫn SCST trên RTX 3090 chỉ mất vài giờ đến một ngày. Trích đặc trưng vùng: GRIT dùng Deformable DETR, không cần Faster R-CNN riêng. Scene graph lấy miễn phí từ mệnh đề VSPS đã kiểm chứng (xem 11 §4.1). Baseline LVLM fine-tune (Vintern-1B, Qwen2.5-VL-3B/7B, QLoRA trên caption KTVIC) chạy được trên 3090, ở mức chi phí như SFT VSPS hiện tại.

**Overlap: trung bình-cao.**
- ViG (MAPR 2026) đã làm "GRIT + quan hệ cặp vùng + tri thức văn hóa Việt" trên đúng KTVIC/UIT-ViIC. Nếu đề xuất "relation/KG module trên GRIT" thì bắt buộc phải so với ViG và nêu khác biệt rõ.
- Nhóm Tran/Le/Nguyen (ACIIDS 2025, FAIR 2025) đã làm "KG + ConceptNet captioning", nhưng trên tiếng Anh.
- HDUCap (JVCIR 2026) đã có "spatially-aware transformer" tiếng Việt.

**Novelty: thấp nếu chỉ là kiến trúc, trung bình nếu đổi nguồn tri thức hoặc đổi cách đánh giá.** Những gì **chưa thấy** trong các bài trên:
1. Đồ thị **đã kiểm chứng trên ảnh** (verified scene graph của VSPS) làm giám sát hoặc đầu vào cho captioner nhỏ. ViG học quan hệ ngầm, ACIIDS dùng KG từ detector + ConceptNet không kiểm chứng.
2. So sánh công bằng **captioner nhỏ vs LVLM fine-tune trên cùng train split tiếng Việt**, có cả CIDEr lẫn metric trung thực (CHAIR-vi, graph recall theo 11 §4.2). Hiện các bài chỉ so với LVLM zero-shot (ViTextCaps/GPT-4o) hoặc với "một mô hình lớn hơn" không nêu tên (ViG).
3. Đánh giá bằng metric đồ thị trên caption tiếng Việt. Mọi bài ở §1 chỉ báo BLEU/METEOR/ROUGE/CIDEr, và OpenViIC ghi rõ "SPICE is not used because the Vietnamese language scene graph is unavailable".

**Có vượt được LVLM không?** Trên CIDEr thì gần như chắc: con số 136 của GRIT so với 29,0 (zero-shot) và 17,3 (VSPS) của Qwen là khoảng cách do phong cách caption. Nhưng LVLM fine-tune trên KTVIC có thể thu hẹp khoảng cách này rất nhiều. Chưa có số công bố, nên đây là thí nghiệm phải tự chạy trước tiên. Nếu Qwen2.5-VL-7B QLoRA trên KTVIC đạt từ 130 CIDEr trở lên thì luận điểm "captioner nhỏ vẫn đáng làm" chỉ còn đứng được nhờ hiệu năng (tham số, độ trễ, chạy được trên edge) và độ trung thực.

---

## 4. Khuyến nghị

1. **Thí nghiệm quyết định (khoảng 1 tuần GPU, làm trước mọi thứ khác):** trên KTVIC split chính thức, cùng tokenizer RDRSegmenter, chạy (a) GRIT nhánh vicap, tái lập 136,0; (b) Vintern-1B và Qwen2.5-VL-3B QLoRA trên caption train; (c) Qwen2.5-VL-7B QLoRA. Báo CIDEr, CHAIR-vi, số tham số và ảnh/giây. Kết quả này cho biết ngách có thật hay không.
2. Nếu captioner nhỏ còn hơn rõ: đóng khung bài là **"VSG-Cap: chưng cất verified scene graph của VSPS vào captioner nhỏ"**. Teacher = mệnh đề VSPS đã kiểm chứng. Student = GRIT/ViG-like, với graph encoder trên nút/cạnh đã kiểm chứng, hoặc dùng loss phụ dự đoán bộ ba. Đánh giá bằng CIDEr cùng metric graph-recall/precision (ý 1 trong 11). Baseline bắt buộc: GRIT, ViG (nếu có code/số), MDSANet+CAMO (OpenViIC), LVLM fine-tune. Venue hợp lý: TALLIP, JVCIR, SPIC (Q2). Không nên nhắm Q1.
3. Nếu LVLM fine-tune gần bằng hoặc hơn: bỏ hướng captioner nhỏ. Dồn lực vào đồ thị dùng cho kiểm chứng và đánh giá (11, ý 1 và ý 3), vì ở đó tiếng Việt còn trống thật.
4. Trước khi nộp FAIR/MAPR: xin hoặc đọc toàn văn ViG, HDUCap và FAIR 2025 "Developing a KG for the Image Captioning Problem" để tránh bị nói trùng.

---

## 5. Chưa xác minh / hạn chế
- **Số của ViG** (MAPR 2026) và tên "mô hình đa phương thức lớn hơn đã fine-tune" mà bài so sánh: IEEE Xplore trả trang rỗng, S2 chỉ có abstract.
- **HDUCap** (JVCIR 2026): không có abstract trên S2/Crossref, ScienceDirect trả 403. Chưa biết kích thước dataset hay số trên KTVIC/UIT-ViIC.
- **UIT-OpenViIC bản SPIC**: số có thể khác bản arXiv 2023 dùng ở trên.
- **FAIR 2025 "Developing a Knowledge Graph for The Image Captioning Problem"**: không có abstract, chưa biết dùng dữ liệu tiếng Việt hay không.
- "A multimodal transformer-based architecture for Vietnamese image captioning focusing traffic scenes" (J. Sci. Technol. HaUI, 2025, doi 10.57001/huih5804.2025.414): không có tác giả hay abstract trên S2/Crossref.
- ClipCap++, Top-Down Semantic Refinement (AAAI 2026), ImageEval 2025 overview: chưa đọc toàn văn. Đội thắng ImageEval và việc đội đó dùng LVLM hay không: chưa xác minh.
- `data/results/official-short.json` (CIDEr 8,8) là lần chạy DPO liều cao (theo `scripts/plot_dpo_dose.py`), không phải zero-shot, nên không dùng ở đây.
- Con số Qwen/VSPS trong repo dùng prompt "short" của VSPS, không phải prompt kiểu caption KTVIC, nên khoảng cách so với GRIT bị phóng đại một phần do prompt.
- Không truy được arXiv API và OpenAlex hôm nay (429/hết quota), nên có thể sót preprint 2025-2026 chưa được S2 index.
