# HDUCap and SciRep 2026: overlap check for Paper B+D (LRE) and Paper C (TALLIP)

Date: 2026-10-30. Author: AI agent (Claude). This is a read-only check: no paper or bib file was edited and nothing was committed. Every risk rating and "intact / weakened" call below is **AI opinion**, not a ruling.

## Tóm tắt cho PI (tiếng Việt)

- **HDUCap** (Hoang, Nguyen, Pham, Nguyen; Đại học Hồng Đức; JVCIR 121:104963, 2026; bài có mặt trên Crossref từ 14/09/2026). Bộ dữ liệu có **15.000 ảnh cảnh tự nhiên, mỗi ảnh 5 câu mô tả độc lập do người viết** và nhấn mạnh quan hệ không gian. Đi kèm là một **transformer có nhận biết không gian**, đánh giá theo ba cách: trong miền, zero-shot chéo bộ, và huấn luyện trộn trên UIT-ViIC, VieCap4H, KTVIC. Tác giả tự nhận đây là "bộ mở-miền tiếng Việt lớn nhất, toàn bộ câu do người viết". Bản toàn văn bị khoá. Chúng tôi đã đọc abstract, phần mở đầu và các đoạn trích của mỗi mục qua bản preview công khai, không đăng nhập và không dùng e-mail.
- **Scientific Reports 2026**: Hussain et al., doi 10.1038/s41598-026-70568-5. Bài chỉ làm **tiếng Urdu và Ả Rập**, trên bộ ZARWA-v1 dịch máy từ tiếng Anh. Họ so sánh Qwen2.5-VL, Pangea, PALO, mBLIP, PaliGemma2 và LLaVA-OV ở zero-shot, LoRA và QLoRA. **Không có tiếng Việt và không có in-context/retrieval.** Bài đang ở dạng Accelerated Preview nên chỉ đọc được abstract.
- **Kết luận (ý kiến AI)**:
  - Không có claim "first" nào của B hay C bị phủ định. Đóng góp lõi của B (hai bộ tham chiếu trên **cùng ảnh** và độ dốc theo cỡ dữ liệu huấn luyện) vẫn nguyên. Đóng góp lõi của C (retrieved so với random ở cùng k, đăng ký trước) vẫn nguyên.
  - **Một lỗi sự thật mức CAO ở B**: §2 dòng 5 xếp HDUCap vào nhóm "miền hẹp", trong khi HDUCap là bộ mở-miền.
  - **Mức TRUNG BÌNH**: các câu liệt kê "các benchmark tiếng Việt công khai" ở B §1 và C §1, §2 thiếu HDUCap. Câu "vài nghìn ảnh mỗi bộ" của B và câu "ít và nhỏ" của C không còn đúng.
  - **Mức THẤP–TRUNG BÌNH**: HDUCap đã nhận xét định tính rằng có bộ tiếng Việt "chỉ một người chú thích mỗi ảnh". Phát hiện "5 câu do một người viết" của B nên trích HDUCap. B vẫn là bên **đo định lượng** điều này.
  - SciRep chỉ cần thêm làm trích dẫn phụ (mức thấp).
- **Việc cần làm**: sửa 10 câu nêu ở §4 (B: 8 câu, C: 2 câu), thêm 1 mục bib HDUCap vào `paperC.bib` và 1 mục SciRep vào cả hai file bib. Sau đó build lại `journal_draft_C/tex`. Đề xuất mặc định: writer B và writer C áp dụng nguyên văn ở lượt tick kế tiếp. Đây là thay đổi đảo ngược được.

---

## 1. Sources and what was read

| Paper | Identifier | What was read | How |
|---|---|---|---|
| HDUCap: Hoang, A.C., Nguyen, H.L., Pham, T.-A., Nguyen, D.C. "Benchmarking Vietnamese image captioning: A spatially-aware transformer and the HDUCap dataset." *J. Visual Communication and Image Representation* 121, 104963 (Nov 2026) | doi 10.1016/j.jvcir.2026.104963; PII S1047320326002580 | Abstract; full Introduction with its contribution list; first-paragraph snippets of Sections 2–6 (Related works, The HDUCap dataset, Architecture, Datasets and protocols, Conclusions); reference list (first 30 of 60); keywords | ScienceDirect public article preview, fetched with Firecrawl (no login, no e-mail). A plain curl request got a bot page. Crossref, OpenAlex and Semantic Scholar carry no abstract (all report `closed`). Code and data are released at github.com/long-nguyen12/HDUCap; the GitHub API reports **no licence**. The dataset was not downloaded. |
| SciRep: Hussain, M., Khan, I., Rashid, J., Althobaiti, T., Saleem, M.S., Alameri, A.Q. "Benchmarking large vision language models for multilingual image caption generation in low resource settings." *Scientific Reports* (2026) | doi 10.1038/s41598-026-70568-5 (found via OpenAlex search restricted to Sci Rep, 2026; confirmed on Crossref) | Abstract only. The page is an "Accelerated Article Preview" (unedited manuscript); the `.pdf` URL returns the HTML page; no full text exists yet | nature.com, open access (CC BY-NC-ND 4.0). Received 23 Jun 2026, accepted 3 Sep 2026, published 21 Sep 2026 |

The HDUCap facts used below, with where each one comes from:

- 15,000 natural-scene images, each with **five independent human-written captions**, with emphasis on spatial and locative expressions. Source: Abstract and Introduction.
- Model: positional token embedding for absolute object location, plus a learnable geometric attention bias for relative spatial relations. Source: Abstract and Section 4 snippet.
- Evaluation is in-domain, zero-shot transfer, and mixed-data training on public Vietnamese datasets. The Section 5 snippet names UIT-ViIC, VieCap4H and KTVIC. UIT-OpenViIC is cited (ref. 14) but is not named in that snippet. Source: Abstract and Section 5 snippet.
- The paper claims "steady improvements over strong baselines, especially on higher-order n-gram and consensus metrics". This reads like BLEU-3/4 and CIDEr, but the metric list itself was not visible. Source: Abstract.
- Novelty claim: "to the best of our knowledge … the largest open-domain Vietnamese image captioning dataset created from real-world images and fully human-written Vietnamese captions, without using machine-translated annotations." Source: Section 6 snippet.
- Criticism of prior sets: existing datasets are "narrow in domain coverage", "small in scale (often fewer than 5000 images)", and "lack linguistic variety due to the use of only one caption per image". The dataset section says "only one annotator per image" but does not name which datasets it means. Source: Introduction and Section 3 snippet.
- MLLMs (BLIP-2, LLaVA) are discussed only as motivation. The preview shows no MLLM baseline rows. Source: Introduction.

## 2. Overlap matrix

Legend: ✔ = present in that paper; — = absent; ? = not visible in what we could read.

| Dimension | HDUCap (JVCIR 2026) | SciRep (Hussain et al. 2026) | Paper B+D (LRE) | Paper C (TALLIP) |
|---|---|---|---|---|
| Language | Vietnamese | Urdu, Arabic | Vietnamese | Vietnamese + English arm |
| New dataset | ✔ HDUCap, 15k images × 5 captions, human-written | ✔ ZARWA-v1, translated from English | — (audit of KTVIC; no new captions) | — |
| Image sets | field-collected natural scenes; UIT-ViIC, VieCap4H, KTVIC | ? (source of the English captions not stated in the abstract) | KTVIC, UIT-OpenViIC (same images), UIT-ViIC, XM3600-vi | OpenViIC, KTVIC (memory), XM3600-vi, COCO, NoCaps |
| Model family | trained spatially-aware transformer (region features) | Qwen2.5-VL, Pangea, PALO, mBLIP, PaliGemma2, LLaVA-OV, plus Florence-2, InstructBLIP and BLIP-2 as baselines | Qwen2.5-VL-7B QLoRA SFT (+ supplement VLMs) | Qwen2.5-VL-7B, InternVL3-8B, training-free |
| Adaptation | full training | zero-shot, LoRA, QLoRA | QLoRA SFT | in-context retrieval against random, fixed and zero-shot examples |
| Metrics | n-gram and consensus metrics (BLEU/CIDEr-type, inferred) | BLEU, ROUGE-L, METEOR, chrF, BERTScore, LASER, LaBSE, human evaluation (5 criteria) | CIDEr-D under a stated protocol, object P/R, CHAIR-type | stripped CIDEr-D (vi), PTB CIDEr-D (en), count-matched object precision |
| Cross-dataset evaluation | ✔ zero-shot transfer and mixed-data training, on **different image sets** | — | ✔ two caption panels on the **same images**; training-size slope against both | ✔ out-of-memory test sets (XM3600, NoCaps) |
| Reference independence | asserts 5 independent captions; says prior sets have "one annotator per image" (qualitative) | — | **measures** the single-writer structure of KTVIC (adjacent-share test) | — |
| Protocol and scoring audit (segmentation, punctuation, CIDEr variant) | ? (not visible) | — | ✔ core | partial (stripped scoring) |
| Preregistration, one-look test, CIs | ? (none visible) | — | ✔ | ✔ |
| "First / largest" claim | "largest open-domain Vietnamese, fully human-written" | "not well explored" (Urdu and Arabic) | none (B explicitly makes no SOTA claim) | none ("no priority claim") |

## 3. Claim-by-claim risk (AI opinion)

| # | Claim in our drafts | Paper | Risk | Why |
|---|---|---|---|---|
| R1 | HDUCap is listed as a narrower-domain set (`B sec2_related.md:5`) | B | **high** | This is a factual error: HDUCap describes itself as open-domain natural scenes. A reviewer who knows HDUCap would catch it at once. The fix is easy. |
| R2 | "Public Vietnamese image-captioning benchmarks include UIT-ViIC, KTVIC and UIT-OpenViIC" (`B sec1_intro.md:5`) | B | medium | The list says "include", so it is not closed. Still, it leaves out what may now be the largest general-domain set. |
| R3 | "Vietnamese captioning rests on a few benchmarks of a few thousand images each" (`B sec1_intro.md:7`) | B | medium | UIT-OpenViIC has 13,100 images and HDUCap 15,000. "A few thousand" was already strained and is now wrong. |
| R4 | Single-writer references as the first audit property (`B sec1_intro.md:11`, `sec2_related.md:19`) | B | low–medium | HDUCap raised "one annotator per image" qualitatively as a weakness of earlier Vietnamese sets. B's contribution is the quantitative test on KTVIC, and the KTVIC paper itself documents the interface, so B never claimed discovery. B should still cite HDUCap so the qualitative point is not presented as ours. |
| R5 | "We could not obtain the full text … do not know their split…" and Table 2.1 "not known" (`B sec2_related.md:7`, `:19`, `:29`; `sec7_limitations_ethics.md:22`) | B | low | These remain true for the full text, but the abstract and preview are now readable. The cells can be filled ("no; separate image sets"), and the access note should be dated 2026-10-30. |
| R6 | Two-panel, same-image training-data slope is new (Table 2.1 last row; `sec2_related.md:21` "What we add is narrow") | B | **none–low** | HDUCap's zero-shot and mixed-data transfer runs across **different** image sets and shows no training-size curve in the preview. The B claim stands. This rests on the preview only. |
| R7 | KTVIC protocol audit (punctuation, segmentation, CIDEr variant) | B | none | Nothing in HDUCap or SciRep touches it. |
| R8 | Qwen2.5-VL QLoRA fine-tune as the controlled system | B | low | SciRep also finds Qwen2.5-VL+QLoRA best, for Urdu and Arabic. B claims no novelty for the recipe. SciRep can serve as an optional supporting citation. |
| R9 | "The public Vietnamese benchmarks are UIT-ViIC, KTVIC, UIT-OpenViIC and XM3600" (`C 02_related_work.md:19`) | C | medium | This is a closed list ("are"), so it is now incomplete. A reviewer could also ask why HDUCap was not used as another out-of-memory Vietnamese test. Answer: its licence is unstated on its release page, and C's test sets were fixed in the registration. |
| R10 | "The public general-domain Vietnamese sets are few and small" (`C 01_introduction.md:12`) | C | medium | HDUCap has 15k images and 5 human references. "Small" holds only against COCO. |
| R11 | Retrieved vs random in-context examples, equal k, preregistered, Vietnamese and English (C core, `02:45–50`) | C | **none** | Neither paper does in-context or retrieval captioning. |
| R12 | "Multilingual systems … rely on … data translated from English" (`C 01:12`); "captioning data in languages other than English are often small or translated from English" (`B sec1:7`) | B, C | none (support) | Both new papers support this point. HDUCap criticises machine-translated COCO-VN, and SciRep's ZARWA-v1 is translation-derived. These are optional citations. |

## 4. Exact sentences to change, with proposed replacements

Each `.md` line holds a whole paragraph, so each entry quotes only the sentence to replace. Keep every existing `<!-- src -->` comment. For C, the tex in `journal_draft_C/tex/` (body.tex, paperC.tex) must be regenerated after the `.md` edits. Do not hand-edit the tex.

### Paper B+D (`manuscript/journal_draft_B/`)

**B1. `sec1_intro.md:5` (R2)**
- Current: "Public Vietnamese image-captioning benchmarks include UIT-ViIC (Lam et al., 2020), KTVIC (Pham et al., 2024) and UIT-OpenViIC (Bui et al., 2026), with further sets for narrower domains (Section 2)."
- Proposed: "Public Vietnamese image-captioning benchmarks include UIT-ViIC (Lam et al., 2020), KTVIC (Pham et al., 2024), UIT-OpenViIC (Bui et al., 2026) and HDUCap (Hoang et al., 2026), with further sets for narrower domains (Section 2)."

**B2. `sec1_intro.md:7` (R3, R12)**
- Current: "Vietnamese captioning rests on a few benchmarks of a few thousand images each (Lam et al., 2020; Pham et al., 2024; Bui et al., 2026), and captioning data in languages other than English are often small or translated from English (van Miltenburg, 2024)."
- Proposed: "Vietnamese captioning rests on a few benchmarks of between a few thousand and about fifteen thousand images each (Lam et al., 2020; Pham et al., 2024; Bui et al., 2026; Hoang et al., 2026), and captioning data in languages other than English are often small or translated from English (van Miltenburg, 2024; Hussain et al., 2026)."
- Add the source comment `<!-- src: HDUCap 15,000 images: Hoang et al. 2026 abstract/introduction (ScienceDirect preview, read 2026-10-30); OpenViIC 13,100: Table 2.1 -->`.

**B3. `sec1_intro.md:11` (R4).** Append one sentence at the end of item 1, after its last `<!-- src -->` comment. Inserting it mid-item would separate numbers from their src comments.
- Add: "Hoang et al. (2026) note that some Vietnamese sets have one annotator per image; here we test what that design does to KTVIC's references."

**B4. `sec2_related.md:5` (R1).** This is the high-risk item.
- Current: "Vietnamese captioning data also exist for narrower domains: the VLSP 2021 VieCap4H challenge on healthcare images (Le et al., 2022), the HDUCap dataset (Hoang et al., 2026) and a scene-text captioning dataset (N.N.-Y. Nguyen et al., 2026)."
- Proposed (two sentences): "HDUCap (Hoang et al., 2026) adds 15,000 natural-scene images, each with five captions that its authors describe as independently written, with an emphasis on spatial expressions. Vietnamese captioning data also exist for narrower domains: the VLSP 2021 VieCap4H challenge on healthcare images (Le et al., 2022) and a scene-text captioning dataset (N.N.-Y. Nguyen et al., 2026)."
- Place the HDUCap sentence after the UIT-OpenViIC sentence, before XM3600.

**B5. `sec2_related.md:7` (R5)**
- Current: "We could not obtain the full text of either paper (publisher, IEEE Xplore and Crossref, 2026-10-15), so we do not know their split, word segmentation, CIDEr variant or scale; we report none of their numbers and do not use them as comparators."
- Proposed: "For HDUCap we could read only the abstract and the publisher's preview (2026-10-30), which report in-domain, zero-shot and mixed-data evaluations on UIT-ViIC, VieCap4H, KTVIC and HDUCap; for ViG we could not obtain the full text (2026-10-15). We therefore do not know either paper's split, word segmentation, CIDEr variant or scale; we report none of their numbers and do not use them as comparators."

**B6. `sec2_related.md:19` (R4, R5)**
- Current (last sentence): "HDUCap (Hoang et al., 2026) adds a further dataset with a spatially-aware transformer; we could not access its full text, so we cannot say whether it uses a second reference set."
- Proposed: "HDUCap (Hoang et al., 2026) points out that some Vietnamese sets have one annotator per image and collects five independently written captions per image instead; its cross-dataset evaluations (zero-shot transfer and mixed-data training) use different image sets, not a second reference set for the same images (abstract and publisher preview; full text not accessible to us)."

**B7. `sec2_related.md:29` (Table 2.1 row, R5, R6)**
- Current: `| HDUCap (Hoang et al., 2026) | Vietnamese captioning | new dataset and a spatially-aware transformer | not known (full text not accessible to us) | not known |`
- Proposed: `| HDUCap (Hoang et al., 2026) | Vietnamese captioning, 15,000 images | new dataset and a spatially-aware transformer; in-domain, zero-shot and mixed-data evaluation | no (separate image sets, per abstract and preview) | not stated in the preview |`
- Update the table's source comment: "HDUCap from abstract and ScienceDirect preview (Firecrawl, no login), 2026-10-30; full text closed."

**B8. `sec7_limitations_ethics.md:22` (R5)**
- Current: "…and HDUCap and ViG could not be obtained in full text (Section 2)."
- Proposed: "…and the full texts of HDUCap and ViG could not be obtained (for HDUCap only the abstract and publisher preview; Section 2)."

**B, optional (R8).** In `supplementary_B.md`, where the QLoRA recipe is described, a citation to Hussain et al. (2026) could note that QLoRA on Qwen2.5-VL was also the strongest setting in Urdu and Arabic captioning. This is support only. Skip it if space is tight.

### Paper C (`manuscript/journal_draft_C/`)

**C1. `01_introduction.md:12` (R10, R12)**
- Current: "The public general-domain Vietnamese sets are few and small, and each was built for its own domain and reference style [@Lam2020UITViIC; @Pham2024KTVIC; @Bui2023OpenViIC]; other Vietnamese sets target a single domain, …"
- Proposed: "The public general-domain Vietnamese sets are few and far smaller than English ones such as COCO, and each was built for its own domain and reference style [@Lam2020UITViIC; @Pham2024KTVIC; @Bui2023OpenViIC; @Hoang2026HDUCap]; other Vietnamese sets target a single domain, …"
- Optional, in the same paragraph: "…which brings translation artefacts into the output [@Vu2025VELVET; @Ibrahim2025CONCAP]" → "…[@Vu2025VELVET; @Ibrahim2025CONCAP]; a recent benchmark of open VLMs for Urdu and Arabic captioning is likewise built on translated captions [@Hussain2026SciRepLVLM]."

**C2. `02_related_work.md:19` (R9)**
- Current: "The public Vietnamese benchmarks are UIT-ViIC [@Lam2020UITViIC], KTVIC [@Pham2024KTVIC], UIT-OpenViIC [@Bui2023OpenViIC; @Bui2026OpenViICJournal] and the Vietnamese references of XM3600 [@Thapliyal2022XM3600]."
- Proposed: "Public Vietnamese benchmarks include UIT-ViIC [@Lam2020UITViIC], KTVIC [@Pham2024KTVIC], UIT-OpenViIC [@Bui2023OpenViIC; @Bui2026OpenViICJournal], HDUCap [@Hoang2026HDUCap], whose 15,000 natural-scene images carry five human-written captions each and which comes with a spatially-aware trained transformer, and the Vietnamese references of XM3600 [@Thapliyal2022XM3600]."
- Add after "…our study uses only general-domain sets.": "HDUCap is not among our test sets: our test sets were fixed in the registration, and its release page states no licence."
- Optional, after the AfriCaption sentence: "@Hussain2026SciRepLVLM benchmark open VLMs for Urdu and Arabic captioning in zero-shot, LoRA and QLoRA settings, without in-context examples."
- Before using the licence clause, check the GitHub repository once more for a LICENSE file. As of 2026-10-30 the API reports none.

**C, no change needed (R11).** Table 1 and "What is new" (`02:27–50`) stay as they are. Neither new paper uses in-context examples or retrieval. Adding HDUCap to Table 1 would be off-topic: it is a trained captioner with no retrieval.

## 5. Bib entries to add

`journal_draft_B/paperB.bib` already contains `hoang2026hducap` (lines 91–99). No change is needed except an optional `note`.

Add to `journal_draft_C/paperC.bib` (C's key style):

```bibtex
@article{Hoang2026HDUCap,
  author  = {Hoang, Anh Cong and Nguyen, Hoang Long and Pham, The-Anh and Nguyen, Dinh Cong},
  title   = {Benchmarking {Vietnamese} image captioning: A spatially-aware transformer and the {HDUCap} dataset},
  journal = {Journal of Visual Communication and Image Representation},
  year    = {2026},
  volume  = {121},
  pages   = {104963},
  doi     = {10.1016/j.jvcir.2026.104963}
}
```

Add to both bib files (key `Hussain2026SciRepLVLM` in C; `hussain2026benchmarking` in B to match B's style):

```bibtex
@article{Hussain2026SciRepLVLM,
  author  = {Hussain, Muzammal and Khan, Imran and Rashid, Javed and Althobaiti, Turke and Saleem, Muhammad Shoaib and Alameri, Abdu Qaid},
  title   = {Benchmarking large vision language models for multilingual image caption generation in low resource settings},
  journal = {Scientific Reports},
  year    = {2026},
  doi     = {10.1038/s41598-026-70568-5},
  note    = {Accelerated Article Preview; volume and article number not yet assigned (Crossref, 2026-10-30)}
}
```

The same entry with B's key, for `paperB.bib`:

```bibtex
@article{hussain2026benchmarking,
  author  = {Hussain, Muzammal and Khan, Imran and Rashid, Javed and Althobaiti, Turke and Saleem, Muhammad Shoaib and Alameri, Abdu Qaid},
  title   = {Benchmarking large vision language models for multilingual image caption generation in low resource settings},
  journal = {Scientific Reports},
  year    = {2026},
  doi     = {10.1038/s41598-026-70568-5},
  note    = {Accelerated Article Preview; volume and article number not yet assigned (Crossref, 2026-10-30)}
}
```

Also update `citation_map_B.tsv` and `paperC_bib_audit.tsv` with the new keys. Metadata was verified on Crossref on 2026-10-30, without an e-mail parameter.

## 6. Open items (not blocking)

1. **Image overlap.** It is unknown whether HDUCap images overlap KTVIC or UIT-OpenViIC. "Field-collected" suggests not. Checking would need a download, and the licence is unstated, so it is not recommended unless a reviewer asks.
2. **HDUCap metric protocol.** The segmenter, CIDEr variant and KTVIC numbers are behind the paywall. If the PI's institution has JVCIR access, one full-text read would let B's Table 2.1 and §2 drop "per preview".
3. **SciRep full text.** It does not exist yet (Accelerated Preview). Re-check at the next writer tick. Overlap is expected to stay low.
4. **Which datasets HDUCap criticises.** The "one annotator per image" remark does not name them in the visible snippet. If it names KTVIC in the full text, R4 rises to medium, and B3 should then say "Hoang et al. (2026) also note this for KTVIC".
