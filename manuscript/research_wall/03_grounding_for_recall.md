# 03 — Grounding and perception tools for object recall (research wall, agent 03)

Date: 2026-10-10. Angle: open-vocabulary detectors, SAM-family segmenters, taggers and region captioners, used to give VSPS more true entities before verification and to measure the precision cost.

## 0. Repo grounding: where recall is actually lost (measured today)

I ran `scripts/recall_funnel.py` on the shipped Phase-1a records (`data/stage1_records/stage1_records.tar.gz`, 3,700 KTVIC train images) against `data/supervision/sft.jsonl`. Gold is the 113-entry CHAIR-vi lexicon matched in the KTVIC train references. Because the references are short, P is a lower bound.

| stage | P | R | obj/img |
|---|---|---|---|
| all_props (generator output) | 28.6 | **65.4** | 8.09 |
| not_rejected | 32.2 | 61.9 | 6.81 |
| SUPPORTED | 41.1 | **36.2** | 2.99 |
| SUPPORTED + selected | 43.3 | 33.0 | 2.56 |
| SFT caption | 42.6 | 36.6 | 2.93 |

Extra counts from the same records (my own one-off script, nothing committed):
- **The entity cap discards most of what the generator sees.** Qwen2.5-VL-7B lists a median of 15 objects per image (mean 18.3). `--max-entities 8` (in `configs/main.env` and `scripts/generate_stage1.py`) truncates 86.9% of images, and `generate.py:328-332` keeps the **first 8 in list order**. Nothing ranks the list. The dropped objects are not stored, so their gold rate is unknown.
- **The large drop is the verifier, not the generator.** Entity propositions split into 11,632 SUPPORTED, 11,958 UNCERTAIN and 5,322 REJECTED. For those that contain a lexicon object, the share whose object is in the references (a lower-bound precision) is 43.6% for SUPPORTED, **36.3% for UNCERTAIN** and 15.2% for REJECTED. UNCERTAIN entities are almost as clean as SUPPORTED ones, and there are more of them. Recall falls 61.9 → 36.2 mostly because roughly 41% of entities end up UNCERTAIN.
- **Some "missed" gold is lexical.** The top gold objects absent from all proposals are `người` (506 images), `cô gái` (483), `quầy hàng` (281), `đồ`, `chợ`, `toà nhà`/`nhà`, `cửa`, `đường`, `chàng trai`, `nam thanh niên`, `vỉa hè` and `nón lá`. Gendered person synonyms make up a large share. A detector cannot fix that; the README's "R (gendered → người)" column, 38.0 → 49.4, already covers it. Scene and stuff nouns (`chợ`, `đường`, `vỉa hè`, `quầy hàng`) are where a **tagger** helps and a box detector does not.
- Entities carry no bbox (`entities[*]` keys: id, category_vi, classifier, number, gender, confidence, detector, surface). The geometric spatial check in `verify.py` (`GeometricCheck`, `as_box`) therefore always returns "missing bbox → UNCERTAIN".
- Cost is 83.5 s/image (mean `stats.seconds`, first 500 records).

**Implication:** the grounding tools help most in two places. They can **rank** the generator's existing entity list and **provide a second evidence channel** that moves UNCERTAIN entities to SUPPORTED. They help less by adding new candidates, because R=65.4 at generation is already above the R≥55 target.

## (a) Papers

| # | Paper | Venue / year | Link (opened or confirmed) | Method (1–2 sentences) | Relevance | Action for VSPS |
|---|---|---|---|---|---|---|
| 1 | **Does Object Grounding Really Reduce Hallucination of Large Vision-Language Models?** — G. Geigle, R. Timofte, G. Glavaš | EMNLP 2024 main (ACL Anthology 2024.emnlp-main.159), pp. 2728–2742 | arXiv 2406.14492; aclanthology.org/2024.emnlp-main.159 | Trains LVLMs with referring-expression and grounded-captioning objectives. Finds little to no effect on open-caption object hallucination; grounded captioning at inference slightly cuts hallucination but makes captions less informative. | must-cite; low overlap | Cite it to argue that VSPS uses grounding as **data-time evidence**, not as a training objective. It also predicts the precision/informativeness trade-off reviewers will ask about. |
| 2 | **Describe Anything: Detailed Localized Image and Video Captioning** (DAM) — L. Lian, Y. Ding, … T. Darrell, A. Yala, Y. Cui | ICCV 2025 (CVF open access) | arXiv 2504.16072 | Focal prompt plus localized vision backbone with gated cross-attention for region captions. Uses a semi-supervised data pipeline (DLC-SDP) and introduces DLC-Bench, a reference-free benchmark. | technique-to-borrow; low overlap | Region-caption generator for an attribute pass on SAM/detector crops (English, so it needs translation). DLC-Bench's reference-free positive/negative-attribute scoring is a template for a recall metric that does not depend on short references. |
| 3 | **Grasp Any Region: Towards Precise, Contextual Pixel Understanding for Multimodal LLMs** (GAR) — H. Wang, X. Li, Z. Zhang et al. | ICLR 2026 | arXiv 2510.18876 | RoI-aligned feature replay keeps global context while describing a prompted region and models interactions between several prompts. GAR-1B reportedly beats DAM-3B by 4.5 points on DLC-Bench. | technique-to-borrow | A 1B region model fits next to Vintern-1B on a 3090. It is a candidate region-attribute and relation generator. |
| 4 | **Perceive Anything: Recognize, Explain, Caption, and Segment Anything in Images and Videos** (PAM) — W. Lin et al. | NeurIPS 2025 | arXiv 2506.05302 | SAM 2 plus an LLM through a "Semantic Perceiver". For each prompted region it outputs category, definition, function and caption. Reported 1.2–2.4× faster than prior region models. | technique-to-borrow | One pass gives a mask, a category and a caption per region, i.e. a detector, tagger and region captioner in one model. Use it for an offline entity and attribute pass. |
| 5 | **SAM 3: Segment Anything with Concepts** — N. Carion et al. (Meta) | ICLR 2026 | arXiv 2511.16719 | Promptable concept segmentation: a noun-phrase prompt returns masks for every matching instance. A presence head separates "is it there" from localization; trained with hard negatives; SA-Co benchmark. | technique-to-borrow (verifier channel) | The presence head is effectively an existence verifier. Query it with each entity's English head noun. Its mask count is also an independent `counting` check. |
| 6 | **SAM 2: Segment Anything in Images and Videos** — N. Ravi et al. | arXiv 2408.00714 (abs page lists no venue; widely cited as ICLR 2025, not confirmed here) | arXiv 2408.00714 | Promptable image and video segmentation with memory. | background | Use it only if masks are needed for region crops; SAM 3 supersedes it here. |
| 7 | **Scaling Open-Vocabulary Object Detection** (OWLv2) — M. Minderer, A. Gritsenko, N. Houlsby | NeurIPS 2023 | arXiv 2306.09683 | OWL-ST self-training on web image-text pseudo-boxes. LVIS-rare AP rises from 31.2 to 44.6 (L/14). | technique-to-borrow | A text-queried detector with calibrated per-query scores. Use it as the existence channel and as the bbox source for `GeometricCheck`. HF transformers already supports it, so no new framework. |
| 8 | **Grounding DINO 1.5** (arXiv 2405.10300) / **DINO-X** (arXiv 2411.14347) — IDEA Research | arXiv 2024 (DINO-X v3 May 2025) | both abs pages | Open-set detectors. DINO-X adds prompt-free "universal object prompt" detection, i.e. detect-everything mode. Self-reported 56.0 COCO AP / 59.8 LVIS-minival (Pro). | baseline tool | DINO-X Pro is API-only. The open Grounding DINO (2303.05499) is the reproducible choice. Prompt-free mode would add candidates, but candidates are not the bottleneck (§0). |
| 9 | **YOLO-World: Real-Time Open-Vocabulary Object Detection** — T. Cheng et al. | CVPR 2024 | arXiv 2401.17270 | Re-parameterizable VL-PAN with region-text contrastive loss. 35.4 LVIS AP at 52 FPS (V100). | technique-to-borrow (cost) | The cheapest existence channel, in milliseconds per image. |
| 10 | **YOLOE: Real-Time Seeing Anything** — A. Wang, L. Liu, H. Chen, Z. Lin, J. Han, G. Ding | ICCV 2025 (arXiv comments) | arXiv 2503.07465 | Text-prompted, visual-prompted and prompt-free detection and segmentation in one real-time model, the successor to YOLO-World. | technique-to-borrow (cost) | Its prompt-free mode is a cheap "list everything" candidate source that could stand in for a second VLM pass. |
| 11 | **Florence-2: Advancing a Unified Representation for a Variety of Vision Tasks** — B. Xiao, H. Wu, … L. Yuan | CVPR 2024, DOI 10.1109/CVPR52733.2024.00461 | arXiv 2311.06242; mlanthology CVPR 2024 | Seq2seq model (0.23B/0.77B) for `<OD>`, `<DENSE_REGION_CAPTION>`, `<CAPTION_TO_PHRASE_GROUNDING>` and more, trained on FLD-5B. | technique-to-borrow | `<CAPTION_TO_PHRASE_GROUNDING>` on the translated entity list returns a box per phrase, which supplies the missing bboxes. At 0.77B it fits easily next to Vintern-1B. |
| 12 | **Open-Set Image Tagging with Multi-Grained Text Supervision** (RAM++; v1 titled "Recognize Anything Plus Model") — X. Huang et al. | arXiv 2310.15200 (one listing says ACM MM 2025; **unconfirmed**) | arXiv 2310.15200 | Tagging model aligning image-tag and image-text supervision, with LLM-expanded tag descriptions for open-set tags. Reported +5.0 mAP over CLIP on OpenImages open-set. | technique-to-borrow | Covers scene and stuff tags (`market`, `street`, `sidewalk`, `stall`), which is exactly the missed-gold class in §0 that box detectors handle poorly. |
| 13 | **LLMDet: Learning Strong Open-Vocabulary Object Detectors under the Supervision of Large Language Models** — S. Fu et al. | CVPR 2025 | arXiv 2501.18954 | Co-trains a Grounding-DINO-style detector with an LLM caption loss on GroundingCap-1M. | technique-to-borrow | The detector was trained to align with long captions, so it is a good choice for checking caption-derived phrases. A drop-in alternative to Grounding DINO. |
| 14 | **GLaMM: Pixel Grounding Large Multimodal Model** — H. Rasheed et al. | CVPR 2024 | arXiv 2311.03356 | Grounded conversation generation: every noun phrase in the caption carries a mask. | related (already in novelty/06 C5') | Mention it only as grounded-caption prior art. |
| 15 | **Osprey: Pixel Understanding with Visual Instruction Tuning** — Y. Yuan et al. | CVPR 2024 | arXiv 2312.10032 | Mask-level instruction tuning for region understanding. | related | Cite it in the region-captioning related work, next to DAM, GAR and PAM. |
| 16 | **The All-Seeing Project V2: Towards General Relation Comprehension of the Open World** (ASMv2) — W. Wang et al. | ECCV 2024 | arXiv 2402.19474 | Relation conversation: captions with grounded subject-predicate-object triples. | related (already in novelty/06) | Its relation-grounding format parallels VSPS's typed relation propositions. Cite it; low overlap. |
| 17 | **URECA: Unique Region Caption Anything** — S. Lim et al. | arXiv 2025 (no venue listed) | arXiv 2504.05305 | Multi-granularity region captions made unique through a stage-wise MLLM pipeline plus mask encoder. | related | Low priority. |
| 18 | **Semantic-Spatial Agreement Verification for Mitigating Object Hallucination in MLLMs** (SSAV) — Z. Ren et al. | arXiv 2609.17269 (15 Sep 2026, preprint) | arXiv abs | Training-free object verification that fuses semantic support from several paraphrased prompts with query-induced regional persistence (geometric mean). LLaVA-1.5 CHAIRs drops from 49.4 to 32.8. | **medium overlap** with VSPS's multi-query verification idea; inference-time, not data-time | Cite it and contrast: VSPS verifies offline, emits three states and trains on the result. Borrow the "semantic × spatial" geometric-mean fusion for the detector channel (action A2). |
| 19 | **GAVEL: Grounded Caption Error Verification and Localization** — Z. Gao, A. Hashimoto, K. Saito | arXiv 2606.26923 (Jun 2026) | arXiv abs | Task, dataset and benchmark: detect image-text misalignment, explain it, and localize the visual evidence. | metric/benchmark; low overlap | A candidate external test of the verifier, i.e. can Vintern plus a detector localize its own REJECTED decisions. |
| 20 | **Benchmarking LVLMs via Directed Scene Graph for Comprehensive Image Captioning** (CompreCap) — F. Lu et al. | CVPR 2025, DOI 10.1109/CVPR52734.2025.01827 | arXiv 2412.08614 | Segmentation-based object coverage, attribute and relation scores on 560 COCO-panoptic images. | metric/benchmark (already in novelty/06) | Its mask-based object coverage is the right recall metric once VSPS has boxes; it avoids the short-reference lower bound. |

Already in the wall and not repeated here: Image Textualization, SENTINEL, HalluciDoctor, CapMAS, FuseCap, DenseFusion, VFC, Woodpecker, "Generating Accurate and Detailed Captions for High-Resolution Images" (2510.27164; detector-verified co-occurring objects; this is the closest detector-for-recall pipeline and is in novelty/06 A11), ReflectCAP, DetailVerifyBench.

### Unverified
- GroundSight (arXiv 2509.25669, KDD Cup 2025 workshop): bbox crop for VQA RAG. Its relevance to captioning is weak, so it is not in the table.
- RAM++ at ACM MM 2025: seen on one aggregator only.
- SAM 2 at ICLR 2025: not stated on the arXiv page I opened.
- No 2025–2026 paper found that reports **object recall vs. precision for detector-ranked proposition generation in training-data construction**. That gap is VSPS's to claim, carefully.

## (b) Overlap risks (max 5)
1. **SSAV (2609.17269, Sep 2026):** fuses several semantic queries with spatial evidence to verify objects. It is close to "dual-query + K samples". It is distinct because it runs at inference, is binary, covers objects only and does not train. Cite it in the Q2 version.
2. **"Generating Accurate and Detailed Captions for High-Resolution Images" (2510.27164):** an LLM proposes co-occurring objects and a detector verifies them, which is detector-for-recall. If VSPS adds a detector channel, this becomes the closest prior. VSPS's distinction must stay the typed three-state propositions plus neutralization, not the detector.
3. **Image Textualization / SENTINEL (already flagged HIGH / medium-high):** adding a detector makes VSPS look *more* like these. The detector must be framed as one evidence channel inside the existing E-aggregator, not as the verifier.
4. **DAM / PAM / GAR:** low overlap, since they caption regions and do not build verified SFT data. A reviewer may still ask why VSPS does not simply use a region captioner. Answer: they are English-only and unverified, and Geigle et al. show grounding alone does not cut hallucination.
5. **GLaMM / ASMv2 grounded captions:** low overlap. They become relevant only if VSPS outputs boxes, which it does not need to.

## (c) Must-compare baselines / must-cite (max 5)
1. Geigle et al., EMNLP 2024: must-cite; it is the evidence that grounding is not free precision.
2. An **OWLv2 or Grounding-DINO "detector-only filter" ablation**: SUPPORTED = detector score ≥ τ, with no VLM verification. This is the IT/SENTINEL-style baseline reviewers will want in order to see what the VLM verifier adds. It is cheap to run (A4).
3. SAM 3 (ICLR 2026): cite it as the current concept-presence model, and as a possible verifier channel.
4. DAM (ICCV 2025) plus GAR (ICLR 2026): cite them as the region-captioning state of the art in related work.
5. CompreCap (CVPR 2025): report mask-based object coverage on its 560 images, as an English-side recall check with no short-reference bias.

## (d) Actionable improvements for VSPS (ranked by expected gain / cost)

**A1. Rank before truncating, not first-8 (no new model).** Cost: about 0 GPU-h on the generation side.
- *Change:* in `rescap/pipeline/generate.py:generate()`, replace `entities = entities[:max_entities]` with a sort by a priority key, then truncate. The baseline key needs no detector: give lexicon nouns priority (`rescap.chair.objects_in(surface)` non-empty) and deduplicate head nouns (`category_vi`). Once A2 exists, the detector score becomes the key. Keep the truncation note.
- *Effect:* the top 8 gain more lexicon-gold objects. All-props recall should rise and precision is roughly unchanged, because the same number of entities pass to verification. This is a guess. Measure with `scripts/recall_funnel.py` on a 300-image re-run.
- *GPU:* 300 images × 83.5 s ≈ 7 h on a 3090 for the check. This step needs no new compute.
- *Risk:* low. Generic lexicon-first ranking could push out non-lexicon content that the human audit valued (e.g. `áo dài`), which is why the key should be "priority", not "filter".

**A2. Detector existence channel to move UNCERTAIN entities to SUPPORTED (the single best idea).**
- *Change:*
  - (i) Translate each entity head noun to English with the generator already in VRAM (one Qwen call per image, listing all heads), or with a static map for the 113 lexicon nouns.
  - (ii) Run OWLv2-B/16 (HF `Owlv2ForObjectDetection`) or Florence-2-large `<CAPTION_TO_PHRASE_GROUNDING>` once per image on that list.
  - (iii) Write `bbox` and `det_score` onto `entities[*]`.
  - (iv) In `rescap/pipeline/verify.py`, add the detector as a `channel` `EvidenceSignal` for `entity` and `counting` propositions. A Vintern UNCERTAIN with `det_score ≥ τ_hi` becomes SUPPORTED. A Vintern SUPPORTED with no detection at a low threshold is downgraded to UNCERTAIN only for lexicon-countable objects, never for stuff or scene nouns. Fuse the two channels SSAV-style (geometric mean) rather than max, so one weak channel cannot carry the decision.
  - (v) The same bboxes feed the existing `GeometricCheck`, which today always returns "missing bbox".
- *Expected effect:* about 11,958 UNCERTAIN entities exist, with a 36.3% lower-bound gold rate. If a detector at τ_hi accepts the half with higher gold rate, entity-level SUPPORTED recall moves a large step from 36.2 toward the not_rejected ceiling of 61.9. Precision at the SUPPORTED stage stays near 40 only if τ_hi is tuned on the human audit set (`data/human_eval`, `data/object_gold`). Spatial-relation propositions also become decidable. Hallucination: the downgrade arm removes some of the 36.9% wrong-SUPPORTED cases from the human audit. No numbers are claimed; calibrate τ on `data/object_gold` first.
- *GPU:* OWLv2-B/16 or Florence-2-large take under about 2 GB VRAM in fp16 and well under 1 s per image on a 3090 (estimate, not measured), so roughly +1 h over 3,700 images. The verifier stays at 83 s per image. Optional cost cut: if the detector is very confident either way, skip the K=5 Vintern samples for that entity proposition.
- *Risk:* medium. English detector vocabulary misses Vietnamese-specific objects (`nón lá`, `áo dài`, `xe máy` sometimes), so absence of a detection must never REJECT. The paper narrative has to keep the detector as one channel (see the overlap risks with IT and SENTINEL).

**A3. Tagger for scene and stuff nouns (RAM++).**
- *Change:* run RAM++ once per image. Map its English tags to lexicon nouns (`chợ`/market, `đường`/street/road, `vỉa hè`/sidewalk, `quầy hàng`/stall, `toà nhà`/building, `sông`/river). Use them two ways: (a) as an extra existence channel for those classes in `verify.py`; (b) to append missing scene entities to the candidate list in `generate.py` with `generator="ram++"`. They stay `verification.status=None`, so the "generator proposes, never asserts" invariant holds.
- *Effect:* targets the missed gold in §0 (`chợ` 173 images, `vỉa hè` 107, `đường` 133, `quầy hàng` 281, `toà nhà`/`nhà` 330). Precision cost is small if they still pass the Vintern verifier. Scene nouns render as a sentence opener such as "Trong một khu chợ…", so the budget-9 selection cost is one slot.
- *GPU:* the Swin-L tagger is small and runs in under a second per image (estimate).
- *Risk:* low to medium. Tag-to-Vietnamese mapping needs a hand table of about 40 entries for the stuff nouns.

**A4. Detector-only and detector + VLM ablation rows (reviewer defense).**
- *Change:* add a `--verifier-mode {vlm,det,vlm+det}` switch to `scripts/generate_stage1.py`. Run 300 images per mode and score them with `recall_funnel.py` and the human-audit precision.
- *Effect:* no system gain. It answers "why not just a detector (IT/SENTINEL)?" with numbers.
- *GPU:* about 7 h for vlm+det. The det-only mode runs in minutes.
- *Risk:* low. The det-only mode might win on objects, which would itself be a finding and would argue for A2.

**A5. Raise the entity cap only for existence propositions.**
- *Change:* keep `max_entities=8` for the attribute, action and relation passes. Emit existence-only `entity` propositions for entities 9…N that a detector or tagger confirmed (A2/A3), verify them with one dual query at K=5 or the detector channel alone, and let the select.py budget of 9 decide.
- *Effect:* uses the ~10 discarded objects per image (median listed 15 vs cap 8) for little probe cost, because attribute probes dominate time. Precision risk is controlled by requiring detector confirmation.
- *GPU:* about +10–15 s per image if Vintern-verified; about 0 if detector-only.
- *Risk:* medium. Longer entity lists could crowd the 9-slot budget with low-salience objects, so rank by detector box area or score.

**Not recommended now:** DAM, GAR or PAM as attribute generators. They are English-only, add another model (3B–8B) next to Qwen-7B and Vintern on 24 GB, attributes are not the recall bottleneck, and Geigle et al. warn of an informativeness/precision trade-off. Revisit only if attribute recall becomes the target.

## (e) Watch queries (re-run monthly)
1. arXiv listing cs.CV, query: `abs:(detailed caption) AND abs:(open-vocabulary detector OR grounding) AND abs:(hallucination OR recall)`
2. Semantic Scholar, query: `"object coverage" "detailed captioning" detector verification`, sorted by date.
3. Google Scholar alert: `"Describe Anything" OR "Grasp Any Region" OR "Perceive Anything" captioning hallucination`
4. Google Scholar alert: `"SAM 3" OR "Segment Anything with Concepts" hallucination verification caption`
5. OpenAlex, `search=open-vocabulary detection caption hallucination data curation` with filter `from_publication_date:2025-07-01`.
6. arXiv listing, query: `abs:(object hallucination) AND abs:(training-free verification) AND abs:(spatial OR region)`. This catches SSAV-like follow-ups.
