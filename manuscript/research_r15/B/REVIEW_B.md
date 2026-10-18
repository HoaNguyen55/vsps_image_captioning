# R15-B: Literature review for Paper B (Vietnamese captioning system + KTVIC validity audit)

Date: 2026-10-18. Window: 2015 to 2026-10. 70 papers (53 from 2023-2026); full records in `papers_B.json`.

## Verification method

- arXiv: every ID was fetched on its `arxiv.org/abs/` page (title, authors, first-version date, comment, journal-ref), 3.5 s between requests. The export API returned "Rate exceeded" and was not used.
- Journal/proceedings DOIs: checked on `api.crossref.org/works/<doi>` (metadata only), 3.5 s apart.
- Venues come from the arXiv comment / journal-ref or Crossref. Where neither states the venue, the entry is "arXiv" or carries **[UNVERIFIED venue]**. No paper itself is unverified: all 70 resolved on a primary page.
- One-line findings below are taken from the abstract page, or from earlier repo reviews (R13) that read the abstract. HDUCap, ViG, 30VNFoods and the HaUI paper were verified as **metadata only**; their content is not read and nothing is claimed about it.
- No PDFs were downloaded.

## 1. Vietnamese captioning datasets and models (21)

**Datasets.**
- UIT-ViIC (Lam et al., 2020; arXiv 2002.00175; ICCCI 2020): Vietnamese captions for COCO sports images.
- KTVIC (Pham et al., 2024; arXiv 2401.08100): life-domain dataset, 4,327 images / 21,635 captions. Its annotation set-up is the object of our audit.
- UIT-OpenViIC (Bui, Nguyen, Nguyen; SPIC 140:117430, 2026; doi 10.1016/j.image.2025.117430; preprint arXiv 2305.04166): open-domain benchmark. Cite the journal version.
- HDUCap (Hoang et al., JVCIR 2026; doi 10.1016/j.jvcir.2026.104963): new dataset + spatially-aware transformer. Metadata only.
- Domain datasets: 30VNFoods cuisine captioning (Nguyen et al., LNNS 2025; doi 10.1007/978-3-032-05994-9_8); traffic-scene captioning (J. Sci. Tech. HaUI 2025; doi 10.57001/huih5804.2025.414; Crossref lists no authors). Metadata only.
- ViTextCaps-style scene-text captioning with linguistically informed fusion (Nguyen et al., 2026; arXiv 2604.27712).
- Vietnamese medical image-to-text: PET/CT report data (Nguyen et al., NeurIPS 2025 per arXiv comment; arXiv 2509.24739); ViX-Ray chest X-ray (arXiv 2603.15513).

**Systems and models.**
- GRIT (Nguyen et al., ECCV 2022; arXiv 2207.09666): the transformer captioner most cited as a KTVIC baseline.
- ViG (Vu et al., MAPR 2026; doi 10.1109/mapr72750.2026.11685699): grounded adaptation of transformer captioners for low-resource Vietnamese. Metadata only.
- Vintern-1B (Doan et al., 2024; arXiv 2408.12480): Vietnamese MLLM, a zero-shot captioner.
- ViCLIP-OT (Tran et al., 2026; arXiv 2602.22678): Vietnamese vision-language foundation model trained on UIT-OpenViIC; because 401 of 558 KTVIC test images near-duplicate UIT-OpenViIC training images, its scores on KTVIC test risk leakage.
- Text side: PhoBERT (Nguyen & Nguyen, Findings EMNLP 2020; arXiv 2003.00744); VnCoreNLP / RDRSegmenter (Vu et al., NAACL 2018 demos; arXiv 1801.01331); BamiBERT (Nguyen et al., 2026; arXiv 2607.02259), which works on raw, unsegmented text.

**Benchmarks and shared tasks.**
- VMMU (Dang et al., 2025; arXiv 2508.13680): Vietnamese multimodal understanding and reasoning.
- AutoViVQA (arXiv 2603.09689) and ViInfographicVQA (arXiv 2512.12424; AI4Research @ AAAI): VQA resources.
- VLSP 2025 MLQA-TSR (Luu et al.; arXiv 2510.20381): the multimodal VLSP 2025 task is legal QA, not captioning.
- DSC2025 ViHallu (arXiv 2601.04711): hallucination detection for Vietnamese **text** LLMs only.

Takeaway: the Vietnamese captioning work found is all dataset construction or architecture. None of it audits how references were written, or reports a protocol signature (segmenter, CIDEr variant, scale, punctuation policy).

## 2. Multilingual and low-resource captioning (8)

- Crossmodal-3600 (Thapliyal et al., EMNLP 2022; arXiv 2205.12522): 3,600 images with captions written natively in 36 languages, Vietnamese among them. It is our independent third reference set.
- PaLI (Chen et al., ICLR 2023; arXiv 2209.06794) and Pangea (Yue et al., 2024; arXiv 2410.16153): multilingual VLMs evaluated on XM3600. Pangea uses multilingual instruction data, partly machine-translated.
- CONCAP (Ibrahim et al., COLM 2025; arXiv 2507.20411): multilingual retrieval-augmented captioning. It notes that captions translated from English add linguistic bias, which is the cost of translate-train.
- Brazilian Portuguese captioning (Bromonschenkel et al., JBCS; arXiv 2602.00393): models trained and tested on native vs translated Flickr30K references. This is the closest low-resource reference-validity study.
- Multilingual CLIP metrics (Gomes et al., Findings NAACL 2025; arXiv 2502.06600): CLIPScore-style metrics keep human correlation across languages. They are a reference-free check that punctuation or single-writer artefacts cannot affect.
- Berger et al. (NAACL 2025; arXiv 2409.16646): across 31 languages, including Vietnamese, who describes an image changes which entities are mentioned. Two independent panels may therefore disagree legitimately.
- MUNIChus (Chen et al., LREC 2026; arXiv 2603.10613): multilingual news-image captioning benchmark.

Takeaway: translate-train and translated references are known to add bias. No study compares a native-Vietnamese benchmark's references with an independent native panel on the same images.

## 3. LVLM fine-tuning and preference/RL for captions (17)

**Backbones.**
- LLaVA (Liu et al., NeurIPS 2023; arXiv 2304.08485).
- Qwen2.5-VL (Bai et al., 2025; arXiv 2502.13923) and Qwen3-VL (Bai et al., 2025; arXiv 2511.21631). The Qwen3-VL entry closes the "[VERIFY: technical report identifier]" in sec2.
- InternVL3 (Zhu et al., 2025; arXiv 2504.10479): our candidate independent verifier.

**Parameter-efficient SFT and weight averaging.**
- LoRA (Hu et al.; arXiv 2106.09685) and QLoRA (Dettmers et al., NeurIPS 2023; arXiv 2305.14314).
- WiSE-FT (Wortsman et al., CVPR 2022; arXiv 2109.01903) and model soups (Wortsman et al., ICML 2022; arXiv 2203.05482). These are the basis of pending run 59 and the S1 seed soup.

**Sequence-level RL and preference optimisation.**
- SCST (Rennie et al., CVPR 2017; arXiv 1612.00563): optimises CIDEr directly.
- SacreEOS (Hu et al., ICIAP 2023; arXiv 2305.12254): shows that the EOS convention in SCST changes scores, and asks for it to be reported.
- DPO (Rafailov et al., 2023; arXiv 2305.18290) and GRPO (Shao et al., DeepSeekMath; arXiv 2402.03300).
- RLHF-V (Yu et al., CVPR 2024; arXiv 2312.00849) and RLAIF-V (Yu et al.; arXiv 2405.17220): fine-grained human or AI feedback for trustworthiness.
- mDPO (Wang et al., EMNLP 2024; arXiv 2406.11839): conditional preference optimisation, so that DPO does not ignore the image.
- POVID (Zhou et al., 2024; arXiv 2402.11411): AI-generated dispreferred responses.
- VaPR (Wadhawan et al., COLM 2025; arXiv 2510.01700): synthetic preference data carries length and style biases, and the paper builds length-matched hard negatives.

Takeaway: preference and RL methods for LVLMs are judged on English hallucination benchmarks. Few control for caption length or object count. None is tested on a Vietnamese reference-based benchmark against count-controlled baselines.

## 4. Dataset audits, annotation artefacts, metric tokenisation (12)

**Metrics and their reporting.**
- CIDEr (Vedantam et al., CVPR 2015; arXiv 1411.5726): TF-IDF n-gram consensus. IDF is computed over the reference set, so an n-gram the references never use can only lower the score.
- COCO Captions (Chen et al., 2015; arXiv 1504.00325): human-agreement baselines that treat references as independent samples.
- sacreBLEU (Post, WMT 2018; arXiv 1804.08771): tokenisation and reference settings move BLEU, so it reports a version signature. This is the template for our protocol card.
- CLIPScore (Hessel et al., EMNLP 2021; arXiv 2104.08718): reference-free.
- Ilinykh et al. (INLG 2025; arXiv 2511.04754): the choice of scorer can invert captioning conclusions.
- CapArena (Cheng et al., Findings ACL 2025; arXiv 2503.12329): metric biases flip model rankings for detailed captions.

**Artefacts and label quality.**
- Annotation artefacts in NLI (Gururangan et al., NAACL 2018; arXiv 1803.02324): the annotation process leaves exploitable regularities.
- Rater equivalence (Resnick et al., 2021; arXiv 2106.01254): evaluation with human labels assumes independent raters.
- Penquitt et al. (2026; arXiv 2609.21822): detection benchmarks are incomplete; missing labels dominate and change scores.

**Hallucination metrics.**
- CHAIR (Rohrbach et al., EMNLP 2018; arXiv 1809.02156).
- POPE (Li et al., EMNLP 2023; arXiv 2305.10355).
- AMBER (Wang et al., 2023; arXiv 2311.07397): LLM-free and multi-dimensional.
All three rely on English object lexicons.

Takeaway: tokenisation and convention effects are documented for BLEU and for the EOS token in SCST. For Vietnamese captioning, no work found quantifies the effect of word segmentation or of punctuation absent from the references. Annotation-artefact audits exist for NLI and for detection labels, but not for a captioning benchmark's writer design.

## 5. Evidence-adding hallucination mitigation (12)

**Decoding and post-hoc correction.**
- VCD (Leng et al.; arXiv 2311.16922) and OPERA (Huang et al., CVPR 2024; arXiv 2311.17911).
- Woodpecker (Yin et al., Sci. China Inf. Sci. 2024; arXiv 2310.16045): post-hoc correction using external detectors.
- LURE (Zhou et al., ICLR 2024; arXiv 2310.00754): a learned revisor.

**Detectors and verifiers.**
- Grounding DINO (Liu et al.; arXiv 2303.05499): an open-set detector, the evidence source for our detector-veto analysis.
- M-HalDetect (Gunjal et al., AAAI 2024; arXiv 2308.06394): a hallucination detector and dataset.
- REVERSE (Wu et al., NeurIPS 2025; arXiv 2504.13169): generate-then-verify with retrospective resampling.

**Hallucination-aware preference data.**
- HA-DPO (Zhao et al.; arXiv 2311.16839).
- HSA-DPO (Xiao et al.; arXiv 2404.14233): severity-aware.
- HALVA (Sarkar et al., ICLR 2025; arXiv 2405.18654): phrase-level alignment.

**Critiques.**
- Fazli et al. (2026; arXiv 2609.01888): mitigation gains often come with lower recall or less detail ("playing it safe").
- Nguyen et al. (IEEE Access 2026 per arXiv comment; arXiv 2610.14976): RL with a CHAIR-only reward is gamed by naming fewer objects, and they propose a consistency+coverage reward.

Takeaway: the evidence comes from detectors, an independent verifier or preference pairs, and gains are reported on English COCO-derived gold. When the "hallucinated" objects are named by an independent human panel, as in about 54% of KTVIC cases (R14 synthesis), a removal method has little room to gain. We found no study that bounds that ceiling with a second reference panel.

## 6. Gaps Paper B fills (no priority claims)

1. **Writer-design audit of a captioning benchmark.** Gururangan et al. and Penquitt et al. audit NLI and detection data, and Resnick et al. formalise rater independence. Paper B measures how KTVIC's single-writer protocol breaks reference independence, and compares its references with an independent OpenViIC panel on the same images.
2. **A Vietnamese protocol signature.** sacreBLEU and SacreEOS made BLEU and SCST conventions reportable. Paper B quantifies the segmentation and punctuation effects for Vietnamese CIDEr (a single "." costs 35.17 CIDEr-D; XM3600 drop tied to end-period rate) and proposes a protocol card that names segmenter, CIDEr variant, scale and punctuation policy.
3. **A controlled fine-tuned-VLM baseline.** Prior KTVIC systems are transformer captioners (GRIT, ViG, HDUCap); Vintern and ViCLIP-OT are not evaluated as fine-tuned captioners under a fixed protocol. Paper B reports a 3-seed QLoRA Qwen2.5-VL system with a registered supervision ladder.
4. **Pre-registered negatives for preference/RL on a non-English benchmark.** DPO, GRPO-style RFT and CIDEr-only SCST are tested against count-controlled baselines and reported as they fell.
5. **A ceiling on evidence-adding mitigation.** The second panel bounds what a detector or verifier can gain on KTVIC. Fazli et al. and Nguyen et al. raise the coverage concern on English benchmarks only.
6. **Leakage hygiene for reference-free scoring.** Paper B does not use ViCLIP-OT on KTVIC test because the model was trained on KTVIC, and uses multilingual CLIP metrics (Gomes et al.) only as a sensitivity check.

## 7. Actions for sec2_related.md

- Replace "[VERIFY]" on XM3600 with EMNLP 2022, arXiv 2205.12522 (verified).
- Replace "[VERIFY: technical report identifier]" for Qwen3-VL with arXiv 2511.21631 (verified).
- "VES-RFT; CCCaption" in the preference paragraph were not checked in this pass: verify them or drop them.
- Consider adding WiSE-FT and model soups (S1, run 59), InternVL3 (S2 verifier), Grounding DINO (detector veto), mDPO/VaPR (DPO negatives), and Gururangan et al. (artefact framing).
- Still open (from R13): read the HDUCap and ViG full texts before citing anything beyond their metadata.

## Open items

- [UNVERIFIED venue] (not found on a primary page in this pass, so cite as arXiv): LoRA, DPO, VCD, RLAIF-V, HSA-DPO, Grounding DINO, Pangea.
- Venues marked "(arXiv comment)" are stated by the authors on arXiv; they were not checked on the venue page.
- The HaUI traffic paper has no author list in Crossref. Fill it in from the journal page before citing.
- Paper A's `papers_*.json` was not found in the repo; the schema follows the task specification.
