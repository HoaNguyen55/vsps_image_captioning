# 04 — Vietnamese and SEA vision-language models, datasets and benchmarks (2025-2026)

Agent 04, 2026-10-10. Scope: which models, datasets and benchmarks released since 2025 matter for VSPS's backbone choices (Vintern-1B verifier, Qwen2.5-VL-7B generator) and its Vietnamese positioning. `../novelty/05_vietnamese_captioning.md` already covers these items, so they are not repeated here: AutoViVQA, ViEduVQA, ViG, HDUCap, ViHallu, VMMU/ViExam, LaVy, Vistral-V, Vista, VLSP 2025 MLQA-TSR, the FAIR 2025 multitask VLM, and the low-resource LMM survey.

How things were checked: arXiv API listings (query `abs:Vietnamese AND (multimodal OR vision OR image)`, sorted by date, 150 results scanned), OpenAlex searches from 2025-06 onward, Hugging Face org listings (5CD-AI, Vi-VLM, SEACrowd, aisingapore, Qwen, OpenGVLab, google), and the MTVQA GitHub leaderboard. Every item below was opened. Numbers marked "self-reported" come from model cards, not from papers.

Repo facts used below:
- `rescap/vlm/registry.py`: the verifier is `5CD-AI/Vintern-1B-v3_5`; `vintern-3b` = `5CD-AI/Vintern-3B-R-beta` is registered but unused; the generator is `Qwen/Qwen2.5-VL-7B-Instruct`.
- `rescap/vlm/vintern.py`: `supports_logprobs = False`. Because of this, `rescap/pipeline/verify.py` (around l.2191) automatically sets `probe_k = SELF_CONSISTENCY_K`. This K=5 sampling is the main reason verification costs ~80 s/image.

## (a) Papers and resources

| # | Title / resource | Authors | Venue, year | Link (opened) | What it is | Relevance to VSPS | Action |
|---|---|---|---|---|---|---|---|
| 1 | **Vintern-1B-v3.5** (model card) | 5CD-AI | HF, created 2025-01-11 | huggingface.co/5CD-AI/Vintern-1B-v3_5 | Fine-tuned from InternVL2.5-1B on Vietnamese data. Self-reported vi-MTVQA 41.9 (v2: 37.4; InternVL2.5-1B: 24.8), OCRBench 706. No hallucination numbers. | This is the verifier already in use. It is still the newest 1B Vintern: the 5CD-AI org has published no newer generative 1B model through 2026-10. | Cite as "Vintern-1B-v3.5 (HF), built on InternVL2.5-1B, technical report arXiv:2408.12480". State the exact checkpoint in the paper. |
| 2 | **Vintern-3B-beta / Vintern-3B-R-beta** (cards) | 5CD-AI | HF, 2024-10-22 / 2025-03-19 | huggingface.co/5CD-AI/Vintern-3B-beta | Qwen2.5-3B-Instruct + InternViT-300M, trained on >10M Vietnamese QA and description pairs. Self-reported Vi-MTVQA 41.29, HallBench 43.22. R-beta is a reasoning variant. No paper. | baseline-to-compare (Vietnamese-specialised zero-shot captioner). Also a candidate verifier upgrade. | Run it zero-shot on the KTVIC test set (registry key `vintern-3b`). |
| 3 | **Vintern-Embedding-1B** | 5CD-AI | HF, 2025-08-26 | HF API listing | Visual-document retrieval embedder. | none (built for documents, not natural images) | Skip. |
| 4 | **Qwen2.5-VL Technical Report** | S. Bai et al. | arXiv 2025 | arXiv:2502.13923 | Current generator. The InternVL3 paper's table gives Qwen2.5-VL-7B MTVQA (9-language average) 29.2 and HallBench 52.9. | Base model. A 2026 reviewer will ask why it is not Qwen3-VL or Qwen3.5. | Keep it as the main backbone. Add a newer-backbone transfer run (see d2). |
| 5 | **Qwen3-VL Technical Report** | S. Bai, Y. Cai, R. Chen et al. | arXiv, 2025-11-26 | arXiv:2511.21631 | Dense models at 2B/4B/8B/32B, MoE at 30B-A3B and 235B-A22B. OCR on 39 languages, >70% accuracy on 32 of them (§5.4). The paper has **no** Vietnamese or MTVQA numbers, and its HallusionBench numbers cover only the 235B model. The 8B card says "32 OCR languages" without listing them. | baseline-to-compare / backbone. Qwen3-VL-8B fits QLoRA on a 3090. | Add Qwen3-VL-8B zero-shot to the KTVIC table, and Qwen3-VL-4B as a verifier ablation. |
| 6 | **Qwen3.5** (model cards; no arXiv paper found) | Qwen team | HF, 2026-02 (0.8B/2B/4B/9B/27B/35B-A3B/…) | huggingface.co/Qwen/Qwen3.5-9B | Natively multimodal through early fusion, with a hybrid Gated-DeltaNet + attention architecture. Claims 201 languages. 9B card: HallusionBench 69.3 and OCRBench 89.2, against 66.0 and 83.9 for Qwen3-VL-30B-A3B. Qwen3.6 (2026-04) and Qwen3.8 (2026-08) also exist, but only at ≥27B. | backbone-to-watch. It is the newest family that fits a 3090, but QLoRA support for the hybrid layers depends on transformers built from main. | Optional: a 9B zero-shot row. Do not migrate SFT to it before the journal deadline. |
| 7 | **InternVL3: Exploring Advanced Training and Test-Time Recipes…** | J. Zhu et al. (OpenGVLab) | arXiv 2025 | arXiv:2504.10479 | Table 7, MTVQA average: InternVL3-1B 22.2, -2B 26.7, -8B 30.2; Qwen2.5-VL-3B 24.8, -7B 29.2. | Gives cited numbers showing that general 7-8B models are only ~30 on MTVQA. | Cite as evidence that Vietnamese-specialised small models compete with them on Vietnamese text tasks. |
| 8 | **InternVL3.5: Advancing Open-Source Multimodal Models…** | W. Wang, Z. Gao, L. Gu et al. | arXiv, 2025-08-25 | arXiv:2508.18265 | 1B to 241B models trained with Cascade RL. Vintern's lineage is InternVL, so this would be the natural base for a future Vintern. | baseline-to-compare (InternVL3.5-8B zero-shot). | Optional zero-shot row. |
| 9 | **Gemma 3 Technical Report** | Gemma Team, A. Kamath et al. | arXiv, 2025-03-25 | arXiv:2503.19786 | 1-27B multimodal models with wider language coverage. Gemma 4 (E2B/E4B/12B/31B) is on HF as of 2026-06; I did not check its specs. | baseline (non-Qwen family, so it avoids the shared-LM-family caveat). | Gemma-3-4B as a candidate cross-family verifier (see d3). |
| 10 | **Gemma-SEA-LION-v4-27B-VL / v4.5-E2B-IT** | AI Singapore / SEACrowd | HF, 2025-10 / 2026-05 | huggingface.co/aisingapore/Gemma-SEA-LION-v4.5-E2B-IT | 27B-VL: ~540k instruction-image pairs in 11 languages, Vietnamese included. v4.5-E2B: built on gemma-4-E2B, takes image input, MIT licence, Vietnamese in post-training. **Neither card reports a vision benchmark.** | SEA-specific baseline / small cross-family verifier candidate. | Mention only. It has no Vietnamese vision evidence yet. |
| 11 | **Crowdsource, Crawl, or Generate? Creating SEA-VL, a Multicultural VL Dataset for Southeast Asia** | S. Cahyawijaya, H. Lovenia et al. (92 authors) | **ACL 2025** (long) | DOI 10.18653/v1/2025.acl-long.916; arXiv:2503.07920 | 1.28M SEA-relevant images. Crawling reaches ~85% cultural relevance; generated images are unreliable for SEA culture. | must-cite (related work on SEA data). It is also a source of Vietnamese-culture images for an out-of-domain stress test. | Cite it. Optionally draw ~300 Vietnam-tagged images as an OOD CHAIR test. |
| 12 | **RICE-VL: Evaluating VLMs for Cultural Understanding Across ASEAN Countries** | T. Pranav, E. Pandey et al. | arXiv 2025-12 | arXiv:2512.01419 | 28k human-curated VQA items plus 1k grounding pairs across 11 ASEAN countries. Proposes the SEA-LAVE metric. | metric/benchmark (low) | Cite in one line. |
| 13 | **MTVQA: Benchmarking Multilingual Text-Centric VQA** | J. Tang, Q. Liu, Y. Ye et al. | **ACL Findings 2025** | arXiv:2405.11985; github.com/bytedance/MTVQA | 9 languages including Vietnamese. GitHub VI column: Qwen2-VL-7B 30.0, Qwen2-VL-72B 41.6, InternVL2.5-78B 41.5, GPT-4o 34.2. | It is the only shared Vietnamese number across models, but it measures **text reading, not object grounding**. | Use it only to explain why Vintern was chosen, and say explicitly that it does not measure what the verifier does. |
| 14 | **ViInfographicVQA** | T.-T. Van-Dinh et al. | AI4Research @ AAAI 2026; arXiv 2025-12 | arXiv:2512.12424 | Vietnamese infographic VQA, single-image ANLS: Ovis2.5-9B 71.02, Qwen2.5-VL-7B 67.42, InternVL3.5-8B 67.02, MiniCPM-o2.6 57.03. | Independent 2025-26 evidence that Qwen2.5-VL-7B is still a top open Vietnamese 7-8B model. | Cite it to justify the backbone. |
| 15 | **ViX-Ray: A Vietnamese Chest X-Ray Dataset for VLMs** | D. V. M. Nguyen, C. T. Truong et al. | **LREC 2026**; arXiv:2603.15513 | DOI 10.63317/3do8tpzockx8 | Fine-tunes Vintern-1B-v3.5, LaVy, InternVL2.5-1B, Qwen2.5-VL (2B as printed, likely 3B), Qwen2.5-VL-7B and MiniCPM-V. Qwen2.5-VL-7B is best. Scores outputs with **GPT-4o atomic-fact precision/recall** and reports "low precision and excessive hallucination". | overlap **low-medium** (atomic-fact P/R on Vietnamese VLM output, medical domain, evaluation only). | Cite it as the precedent for atomic-fact P/R in Vietnamese. Contrast: VSPS uses atomic propositions to *build supervision*, not only to evaluate. |
| 16 | **Linguistically Informed Multimodal Fusion for Vietnamese Scene-Text Image Captioning (ViTextCaps)** | N. N.-Y. Nguyen, A.-D. Nguyen, N. H. Nguyen, K. V. Nguyen, N. L.-T. Nguyen | arXiv 2026-04-30 | arXiv:2604.27712 | New Vietnamese captioning dataset: 15,729 images, 74,970 captions. Graph fusion with phonological attention. No hallucination metric in the abstract. | overlap low. New Vietnamese caption benchmark. | Cite it in the Vietnamese-captioning related work as the newest dataset. |
| 17 | **ViCLIP-OT: The First Foundation VLM for Vietnamese Image-Text Retrieval with Optimal Transport** | Q.-K. Tran, M.-T. Nguyen, N.-K. Pham | arXiv 2026-02-26 (submitted to ESWA) | arXiv:2602.22678 | Vietnamese CLIP trained on UIT-OpenViIC, evaluated on KTVIC and Crossmodal-3600. Beats CLIP and SigLIP on Vietnamese retrieval. The abstract does not say whether weights are released. | technique-to-borrow (cheap Vietnamese image-text scorer) / metric. | If weights are public: cheap entity pre-filter, or a Vietnamese CLIPScore-style reference-free metric (d5). |
| 18 | **ViSignVQA** | H. M. Nguyen, T. L.-T. Dang, K. V. Nguyen | arXiv 2025-12 | arXiv:2512.22218 | Vietnamese signboard VQA: 10,762 images; multi-agent GPT-4 framework. | none | Skip. |
| 19 | **VietMEAgent** | H.-D. Nguyen et al. | **FAIR 2025** (same series as VSPS); arXiv:2511.09058 | arXiv:2511.09058 | Explainable cultural VQA built on program generation and a knowledge base. | none (same venue, so worth one cite) | Optional one-line cite. |
| 20 | **MODL: Composing Domain and Language LoRAs for Cross-Lingual RS MLLMs** | X. Li | arXiv 2026-08 | arXiv:2609.26097 | Orthogonal domain LoRA + text-only language LoRA. Keeps Vietnamese at full strength without paired multimodal data. | technique-to-borrow (low priority) | Watch only. |
| 21 | **Pangea: A Fully Open Multilingual Multimodal LLM for 39 Languages** | X. Yue, Y. Song, A. Asai et al. | arXiv 2024 (late-2024 work) | arXiv:2410.16153 | Multilingual MLLM trained on 6M instructions. | possible multilingual baseline | Low priority. I did not confirm Vietnamese is among the 39 languages. |

### Unverified / not found
- **"ViLLaVA"**: still no model or paper under that name (same result as `Q2_LITERATURE.md`). Do not cite.
- **Vintern-3B technical report**: none exists. Cite the model cards.
- **Vietnamese POPE or any Vietnamese LVLM object-hallucination benchmark**: none found in arXiv, OpenAlex or web searches. VSPS's Vietnamese CHAIR lexicon still looks like the only one (claim C5 holds).
- **VLSP 2025**: the only multimodal task is MLQA-TSR (already in 05). There is no captioning or hallucination task.
- **Qwen3-VL / Qwen3.5 Vietnamese scores**: not reported anywhere I could open. Neither card lists its OCR languages.
- **Gemma 4 specs** and **"A Southeast Asian Language OCR Dataset and Evaluation for LMMs"** (Springer LNCS 2025, DOI 10.1007/978-981-95-3346-6_7): seen in listings only. OpenAlex has no abstract for the latter.

## (b) Overlap risks (max 5)

1. **ViX-Ray (LREC 2026): low-medium.** It also decomposes Vietnamese VLM outputs into atomic facts and reports precision/recall, and it flags hallucination. It is evaluation-only, in a medical domain, scored by a GPT-4o judge. It does not verify or build training targets. One sentence of contrast covers it.
2. **ViTextCaps (arXiv 2604.27712): low.** It is the newest Vietnamese captioning dataset, so a reviewer may ask why VSPS does not use it. Answer: it is scene-text captioning, which is OCR-centred and not object hallucination.
3. **Vintern-3B-beta's own "detailed description" training data: low.** It is trained on >10M Vietnamese descriptions, so a reviewer may ask "why not just use Vintern-3B as the captioner?". The only real answer is the zero-shot baseline in (c).
4. **SEA-VL (ACL 2025): none in method.** The risk is a reviewer seeing it as "SEA captioning data exists". It is image collection only, with no verification.
5. No HIGH-overlap Vietnamese or SEA paper found for 2025-2026.

## (c) Must-compare baselines / must-cite (max 5)

1. **Vintern-3B-beta (or -R-beta) zero-shot on the KTVIC test set**, with the same prompt and CHAIR/P/R/F1 scoring. This is the Vietnamese-specialised baseline a Vietnamese reviewer will ask for first. Registry key `vintern-3b` already exists.
2. **Qwen3-VL-8B-Instruct zero-shot** (arXiv:2511.21631). This is the "is your backbone outdated?" row. If it beats 40.7 F1 zero-shot, that is better found now than by a reviewer.
3. **InternVL3.5-8B zero-shot** (arXiv:2508.18265). This is a non-Qwen family baseline from Vintern's lineage. It ties Qwen2.5-VL-7B on ViInfographicVQA.
4. Must-cite: **SEA-VL** (ACL 2025, DOI 10.18653/v1/2025.acl-long.916) and **MTVQA** (ACL Findings 2025). Use MTVQA explicitly as the reason Vintern was chosen, with the caveat that it measures text reading.
5. Must-cite: **ViX-Ray** (LREC 2026) as the atomic-fact precedent in Vietnamese, and **ViInfographicVQA** (AAAI-W 2026) as independent evidence for Qwen2.5-VL-7B on Vietnamese.

## (d) Actionable improvements, ranked by expected gain / cost

**Answer to Q1 (replace Vintern-1B / Qwen2.5-VL-7B?): no wholesale swap.**
- No newer 1B Vintern exists; v3.5 is already the latest.
- The only cross-model Vietnamese evidence (MTVQA-vi, self-reported) measures OCR, not object/attribute grounding.
- The repo's own measurement shows Vintern weak on colour (precision 0.727 against Qwen2.5-VL's 1.000, `verify.py` ~l.2288).
- So: keep both backbones for the paper's main table, fix the verifier's cost and calibration (d1), and add newer models as baselines and ablations (d2, d3). Choose any replacement by **human-audit precision**, not by public benchmarks.

### d1. Give Vintern token probabilities and drop K=5 sampling (highest gain/cost)
- **Change:** in `rescap/vlm/vintern.py::_generate`, build the prompt the way `chat()` does, then call `self._model.generate(pixel_values=..., input_ids=..., attention_mask=..., output_scores=True, return_dict_in_generate=True, max_new_tokens=1..3)`. InternVL's `generate` forwards kwargs to `language_model.generate`. Return P("Có") / (P("Có") + P("Không")) from the first-step logits. Set `supports_logprobs = True`. `verify.py` then keeps `probe_k=1` with no further edit, because `auto_k` keys on that flag.
- **Effect:**
  - Probe calls drop ~5x, so ~80 s/image becomes an estimated ~16-25 s/image (image tiling is already shared).
  - Confidence becomes continuous rather than a 0/0.2/…/1 agreement fraction. The SUPPORTED threshold can then be tuned against the existing human audit (63.1% SUPPORTED correct) with a simple reliability curve. That is the most direct lever on verifier precision.
- **GPU:** none extra. Re-verification of KTVIC fits overnight on the 3090.
- **Risk:** the yes/no token is not always the first token (whitespace or "Vâng"). Mitigation: sum probability over a small variant set, and keep K=5 as a config flag for the ablation table. One unit test with `mock` should assert the flag routes `probe_k=1`.

### d2. Newer-backbone rows: Vintern-3B and Qwen3-VL-8B zero-shot, plus one VSPS-SFT run on Qwen3-VL-8B
- **Change:**
  - Register `qwen3-vl-8b` in `rescap/vlm/registry.py`. `QwenVLAdapter` should work once transformers ≥4.57 is installed; verify the class name for Qwen3-VL.
  - Run `scripts/evaluate.py` zero-shot for `vintern-3b`, `qwen3-vl-8b` and optionally `internvl3.5-8b` (needs a vintern-style adapter entry with an OpenGVLab model id).
  - Then run the existing SFT recipe with base = Qwen3-VL-8B on the same rendered captions.
- **Effect:** pre-empts the "outdated backbone" critique. If Qwen3-VL-8B zero-shot recall is already >57, then VSPS-SFT on it is the most likely route to the R≥55 / F1>40.7 target, because VSPS precision gains would stack on a higher-recall base.
- **GPU:** zero-shot at ~2-3 h per model on the KTVIC test set; QLoRA SFT of 8B at roughly the current 7B cost (+10-15% VRAM; check `scripts/measure_vram.py`).
- **Risk:** transformers version bump may break the Qwen2.5-VL path, so pin a separate venv. Qwen3.5-9B is newer, but its hybrid DeltaNet layers make bitsandbytes QLoRA a risk. Use it zero-shot only.

### d3. Cross-family second verifier for colour and gender, replacing the Qwen2.5-VL colour check
- **Change:** `verify.py` already sends colour to a second verifier, Qwen2.5-VL, which is the generator's own family (self-verification bias, and Vintern's LM is Qwen too). Swap in, or add, Gemma-3-4B-it or InternVL3.5-4B as the tie-breaker for colour and gender propositions only.
- **Effect:** removes the "everything is Qwen" objection, which `vintern.py` already flags as a caveat. It may also raise precision on the two error-prone types. Measure on the human-audit subset before claiming either.
- **GPU:** 4B in bf16 is about 9 GB, so it co-resides with Vintern-1B. The probe count only rises for colour and gender propositions.
- **Risk:** Gemma's Vietnamese colour vocabulary (xanh lam / xanh lá) is unmeasured. Run `scripts/count_colour_ambiguity.py`-style checks first.

### d4. OOD Vietnamese stress set from SEA-VL or ViTextCaps (cheap evaluation gain)
- **Change:** sample ~300 Vietnam-tagged SEA-VL images and run generation + CHAIR with the Vietnamese lexicon. No gold captions are needed for CHAIR-style proposition audits. Reuse `scripts/build_stress_manifest.py`.
- **Effect:** answers the "KTVIC + translated COCO is narrow" critique with culturally Vietnamese scenes. It does not change model numbers.
- **GPU:** ~1-2 h. **Risk:** licensing of crawled images; publish IDs only.

### d5. Vietnamese image-text scorer (ViCLIP-OT) as a pre-filter / metric (only if weights are released)
- **Change:** run entity propositions through a CLIP similarity gate before the VLM probe. Skip clear negatives, and send only borderline ones to Vintern. Alternatively, report a reference-free Vietnamese CLIP score in `rescap/metrics.py`.
- **Effect:** further cuts probes (entities are the largest proposition type). A new metric column. The effect on recall is neutral to slightly negative if the gate is too strict.
- **GPU:** negligible. **Risk:** weights may be unavailable; CLIP is weak on small objects, so gate only REJECT-side decisions with a conservative threshold.

## (e) Watch queries (re-run monthly)

1. arXiv API: `search_query=abs:Vietnamese AND (abs:multimodal OR abs:vision OR abs:image OR abs:caption*)&sortBy=submittedDate&sortOrder=descending&max_results=50`
2. HF API: `https://huggingface.co/api/models?author=5CD-AI&sort=createdAt&direction=-1` (new Vintern), and the same with `author=aisingapore` / `author=SEACrowd` (SEA-LION VL)
3. OpenAlex: `https://api.openalex.org/works?search=Vietnamese%20vision-language%20model&filter=from_publication_date:2026-06-01`
4. OpenAlex: `search=Vietnamese%20image%20captioning%20hallucination` (watch for a Vietnamese POPE/CHAIR competitor to C5)
5. Semantic Scholar / Google Scholar alert: `"Vietnamese" ("hallucination" OR "CHAIR" OR "POPE") "vision-language"`
6. GitHub watch: `bytedance/MTVQA` leaderboard (Vietnamese column for Qwen3-VL / Qwen3.5 / new Vintern)
