# A-E3 Annex B row B0 v1: model-card row per passing model

Written 2026-11-12T17:37Z (`date -u`). vsps HEAD `f267815`. Writer agent. Not committed. AI opinion where marked. "chưa kiểm" = not checked.

**What B0 is.** Scoring note v1 §2 line 18 (CC-349 ruling 5 / N5): one text row per passing model, printed before any other Annex B row. Columns: language model and vision encoder as read from `config.json` at the pin; Vietnamese output (the G4 share from the pull line); training-data exposure to COCO-vi, UIT-ViIC and XM3600/Crossmodal-3600 from the model card or paper; licence line. No other per-model outcome figure is given here.

**Passing models.** `passed_7a.txt` = aya_vision_8b, smolvlm2_2b, llava16_mistral_7b (LOG OPS-1112aw); `passed_7c.txt` = gemma3_4b_lb26 (LOG OPS-1112bh). Hub ids and revisions from `A_E3_REG_v2.json`.

**Sources used.** `A_E3_ANNEX_B_SCORING_NOTE_v1.md`, `A_E3_ADDENDUM_MODELS_v1.md`, `A_E3_REG_v2.json`; LOG lines OPS-1112bt (config names), OPS-1112aw and OPS-1112bh (G4 shares); public Hugging Face model cards and the papers they cite. Nothing in `data/results/a_e3/`, `data/results/a_cert_e3/`, any prediction file, label file or key file was opened.

**Retrieval date of web sources:** 2026-11-12 (UTC). Card revisions: SmolVLM2 and LLaVA-1.6 cards were read as raw `README.md` at the pinned revision. Aya and Gemma are gated, so the raw file at the revision returned HTTP 401; their public model pages were read instead. On 2026-11-12 the Hub API reported `main` = the pinned revision for both (Aya `d7601ac8…`, Gemma `093f9f38…`), so the page shown is the card at the pin.

**Reading rule for the exposure column.** "stated yes" = the card or the paper it cites says the training data includes the dataset (quote in Sources). "stated no" = it says the dataset was excluded. "not stated" = neither. "not stated" is not "no exposure".

## Table

| Model (hub id @ revision) | Language model: `config.json` → name | Vision encoder: `config.json` → name | Vietnamese output: G4 share, short / detailed (n 50) | Exposure: COCO-vi | Exposure: UIT-ViIC | Exposure: XM3600 / Crossmodal-3600 | Licence |
|---|---|---|---|---|---|---|---|
| Aya-Vision-8B (`CohereLabs/aya-vision-8b` @ `d7601ac8`) | `cohere2` → Command R7B base, post-trained with the Aya Expanse recipe [S1] | `siglip_vision_model` → SigLIP2-patch14-384 [S1] | 1.000 / 1.000 | not stated. Parent COCO: **stated yes** in Cohere's report (not linked from the card): English data partly from MS-COCO, re-captioned, then machine-translated into 22 languages incl. Vietnamese [S2, S3] | not stated | not stated | cc-by-nc-4.0 + Cohere Labs Acceptable Use Policy [S1] |
| SmolVLM2-2.2B-Instruct (`HuggingFaceTB/SmolVLM2-2.2B-Instruct` @ `482adb53`) | `llama` (architecture class only) → SmolLM2-1.7B-Instruct [S4]; not a Llama-family model | `smolvlm_vision` → shape-optimized SigLIP (`siglip-so400m-patch14-384`) [S4] | 1.000 / 1.000 | not stated. Parent COCO: **stated yes** by slice name in the card's training table, `llava-onevision/sharegpt4v_coco`, 1.5 % [S5] | not stated | not stated | apache-2.0 [S4] |
| LLaVA-1.6-Mistral-7B (`llava-hf/llava-v1.6-mistral-7b-hf` @ `2424fdd4`) | `mistral` (`_name_or_path` mistralai/Mistral-7B-Instruct-v0.2) → Mistral-7B-Instruct-v0.2 [S6] | `clip_vision_model` → CLIP ViT-L/14, 336 px (from the LLaVA-1.5 paper; the card does not name it) [S8] | 1.000 / 1.000 | not stated. Parent COCO: not stated for the 760K LLaVA-NeXT set; the cited LLaVA-1.5 paper states COCO-derived data in the 665K mixture that the blog says it modifies [S7, S9] | not stated | not stated | apache-2.0 [S6] |
| Gemma-3-4B-it (`google/gemma-3-4b-it` @ `093f9f38`; run as `gemma3_4b_lb26`) | `gemma3_text` → Gemma 3 4B [S10] | `siglip_vision_model` → 400M SigLIP variant [S11] | 1.000 / 1.000 | not stated. Parent COCO: not stated as training data; COCO Caption appears only as an evaluation benchmark [S10, S11] | not stated | not stated | Gemma Terms of Use [S10] |

The "Parent COCO" note inside the COCO-vi cell is added from the task brief ("COCO or its Vietnamese versions"). It is not a separate column of line 18 (see Open point 10).

`config.json` values: LOG OPS-1112bt-a-e3-config-names (read on HC2 at 14:08:51Z; config sha256 prefixes aya `124b90dcbb6de8ec`, smolvlm2 `ec1f7e45deeafba7`, llava16 `ddf45e24cea7da06`, gemma3 `9059f680f4dbd195`). Top-level `model_type`: `aya_vision`, `smolvlm`, `llava_next`, `gemma3`.
G4 shares: LOG OPS-1112aw (7a pull: "aya 1.000/1.000, smolvlm2 1.000/1.000, llava16 1.000/1.000") and OPS-1112bh (7c pull: "G4 Vietnamese share 1.000 on both prompts (n 50)"). G4 measures only whether captions contain Vietnamese letters or tone marks (addendum §6); it is not a quality measure.

## Sources

Retrieved 2026-11-12 (UTC).

- **[S1]** Aya-Vision-8B card, https://huggingface.co/CohereLabs/aya-vision-8b (main = pinned `d7601ac8…` on the retrieval date).
  - "This is a vision-language model that uses a multilingual language model based on Command R7B and further post-trained with the Aya Expanse recipe, paired with SigLIP2-patch14-384 vision encoder through a multimodal adapter for vision-language understanding."
  - "License: CC-BY-NC, requires also adhering to Cohere Lab's Acceptable Use Policy"
  - "The model has been trained on 23 languages: English, French, … Vietnamese, …" (context for the Vietnamese column; not a B0 cell).
  - The card names no training dataset. It links a blog post, https://huggingface.co/blog/aya-vision; the page's paper list shows arXiv 2412.04261 (the Aya Expanse text model), not the Aya Vision report (no occurrence of `2505.08751` in the page).
  - The blog names the Cauldron ("we first selected images from the Cauldron held-out test set … ensuring they had not been seen during training", about its benchmark) and lists `HuggingFaceM4/the_cauldron` as its one dataset. It does not mention COCO, Open Images, XM3600 or UIT-ViIC.
- **[S2]** Aya Vision technical report, arXiv 2505.08751 ("Aya Vision: Advancing the Frontier of Multilingual Multimodality"), https://arxiv.org/abs/2505.08751, §2.1–2.2.
  - "We constructed our dataset on well-established open-source resources, including Cauldron [Laurençon et al., 2024b] … and PixMo …"
  - "The original dataset is primarily composed of open-source, academic image captioning corpora … Much of the data originates from a narrow set of sources such as MS-COCO [Lin et al., 2014], Visual Genome [Krishna et al., 2017], and Open Images [Kuznetsova et al., 2020]".
  - The report is not linked from the card at the pin; it is Cohere's own report on the same model family. Whether the 8B checkpoint at `d7601ac8` was trained on exactly this mix is not stated in the card (chưa kiểm).
- **[S3]** Same report, §2.4: "we translate our re-annotated English dataset (see §2.2) into the following 22 languages: Arabic, … Turkish, Ukrainian, and Vietnamese." (NLLB-3.3B, then post-editing with command-r-plus-08-2024.) This is the report's own translation, not a named COCO-vi dataset.
- **[S4]** SmolVLM2-2.2B-Instruct card, https://huggingface.co/HuggingFaceTB/SmolVLM2-2.2B-Instruct/raw/482adb537c021c86670beed01cd58990d01e72e4/README.md
  - "SmolVLM2 is built upon [the shape-optimized SigLIP](https://huggingface.co/google/siglip-so400m-patch14-384) as image encoder and [SmolLM2](https://huggingface.co/HuggingFaceTB/SmolLM2-1.7B-Instruct) for text decoder part."
  - "We release the SmolVLM2 checkpoints under the Apache 2.0 license." Front matter: `license: apache-2.0`, `language: - en`.
- **[S5]** Same card, "Granular dataset slices per modality", Image Datasets table: "llava-onevision/sharegpt4v_coco | 1.5%". Training-data sentence: "SmolVLM2 used 3.3M samples for training originally from ten different datasets: LlaVa Onevision, M4-Instruct, Mammoth, LlaVa Video 178K, FineVideo, VideoStar, VRipt, Vista-400K, MovieChat and ShareGPT4Video." The front matter also lists `HuggingFaceM4/the_cauldron` and `HuggingFaceM4/Docmatix`. The SmolVLM paper (arXiv 2504.05299) has no occurrence of "COCO", "Crossmodal", "XM3600" or "Vietnam" (text search of the arXiv PDF).
- **[S6]** LLaVA-1.6-Mistral-7B card, https://huggingface.co/llava-hf/llava-v1.6-mistral-7b-hf/raw/2424fdd47412fccc66d91719126b420e9fbd7065/README.md
  - Title: "LLaVa-Next, leveraging mistralai/Mistral-7B-Instruct-v0.2 as LLM".
  - "LLaVA 1.6 improves on LLaVA 1.5 BY: Using Mistral-7B (for this checkpoint) … More diverse and high quality data mixture".
  - Front matter: `license: apache-2.0`, `language: - en`. The card names no vision encoder and no training dataset; it cites the LLaVA-NeXT blog and arXiv 2310.03744.
- **[S7]** LLaVA-1.5 paper, arXiv 2310.03744 ("Improved Baselines with Visual Instruction Tuning"), https://arxiv.org/abs/2310.03744: "LLaVA [36] is the pioneer to leverage text-only GPT-4 to expand the existing COCO [35] bounding box and caption dataset to a multimodal instruction-following dataset". Table 7 ("Instruction-following Data Mixture of LLaVA-1.5", 665K) lists LLaVA 158K, VQAv2 83K, OKVQA 9K, A-OKVQA 66K, RefCOCO 48K among others.
- **[S8]** Same paper: "namely, using CLIP-ViT-L-336px with an MLP projection".
- **[S9]** LLaVA-NeXT blog, https://llava-vl.github.io/blog/2024-01-30-llava-next/: "We remove TextCaps from our training data …; we replace TextCaps with DocVQA and SynDog-EN. … we further add ChartQA, DVQA, and AI2D"; data sources added: "LAION-GPT-V and ShareGPT-4V" and "a small 15K visual instruction tuning dataset". Model card table: "Stage-1 Training Data 558K … Stage-2 Training Data 760K". The blog does not list the full 760K mixture and does not name COCO.
- **[S10]** Gemma-3-4B-it card, https://huggingface.co/google/gemma-3-4b-it (main = pinned `093f9f38…` on the retrieval date).
  - "Gemma 3 models are multimodal, handling text and image input and generating text output … multilingual support in over 140 languages".
  - Training Dataset: "Web Documents … Code … Mathematics … Images: A wide range of images enables the model to perform image analysis and visual data extraction tasks." No dataset is named.
  - "COCOcap" appears only in the Multimodal benchmark table of the evaluation section. The card names no vision encoder.
  - "Terms of Use: Terms" (link to the Gemma Terms of Use; the repo is gated with manual acceptance).
- **[S11]** Gemma 3 Technical Report, arXiv 2503.19786, https://arxiv.org/abs/2503.19786.
  - "Vision encoder. We use a 400M variant of the SigLIP encoder (Zhai et al., 2023)".
  - "We decontaminate evaluation sets from our pre-training data mixture".
  - COCO Caption appears as an evaluation benchmark, and in Table 12 ("Performance of pre-trained checkpoints after fine-tuning on multi-modal benchmarks"): separate per-task fine-tunes, not the released -it checkpoint. No occurrence of "Crossmodal", "XM3600" or "Vietnam".

## Open points

1. **COCO-vi, UIT-ViIC and XM3600 are "not stated" for all four models.** None of the cards or cited papers names any of them as training data. This is absence of a statement, not evidence of no exposure.
2. **Image-level overlap is open and cannot be settled from cards.**
   - UIT-ViIC images are taken from MS-COCO, and XM3600 images from Open Images (both chưa kiểm here; neither was re-read for this row).
   - Three models state COCO-sourced training data: Aya, SmolVLM2 (slice name) and LLaVA-1.6 (via LLaVA-1.5).
   - Aya's report also names Open Images as a source.
   - So these models may have seen UIT-ViIC or XM3600 *images*, with English (or, for Aya, machine-translated) text, not the Vietnamese references. No card states which images were used.
3. **Aya: Vietnamese COCO-derived text.** The report says the COCO-sourced English set was re-captioned and machine-translated into Vietnamese [S2, S3]. That is Vietnamese text on COCO images, but it is not a named COCO-vi dataset, so the COCO-vi cell stays "not stated". Two further gaps:
   - The report is not linked from the card at the pin.
   - The report's data mix is not tied to the exact `d7601ac8` checkpoint in writing.
4. **SmolVLM2: two gaps.**
   - Its COCO "stated yes" rests on a slice name (`sharegpt4v_coco`), not a sentence.
   - The front matter lists `the_cauldron`, whose sub-collections may include COCO-image sets (chưa kiểm), but the card does not say these were used for SmolVLM2's own training stage. SmolVLM2's `base_model` is SmolVLM-Instruct, whose training data was not read for this row (chưa kiểm).
5. **LLaVA-1.6-Mistral: parent COCO is "not stated" for its own data.** The LLaVA-1.5 paper states COCO-derived data in its 665K mixture. The blog describes the 760K stage-2 set as changes to that mixture without listing it in full, so whether the COCO-sourced parts were kept is implied, not stated.
6. **Gemma 3: COCO is "not stated" for training.** The report's decontamination sentence covers evaluation sets only. It is not read as "stated no" for COCO train images.
7. **Name conflicts between `config.json` and the cards.**
   - (a) SmolVLM2 `text_config.model_type` = `llama` is the architecture class; the card names SmolLM2-1.7B-Instruct. Do not count it as Llama-family (OPS-1112bt note).
   - (b) Aya `vision_config.model_type` = `siglip_vision_model`, while the card says SigLIP2. Transformers loads fixed-resolution SigLIP2 checkpoints with the SigLIP class, so the field cannot tell the two apart. The row follows the card (AI opinion; chưa kiểm against the weights).
   - (c) SmolVLM2 `vision_config.model_type` = `smolvlm_vision` is a SmolVLM-specific class name; the encoder name comes from the card.
   - (d) LLaVA-1.6 and Gemma cards do not name the vision encoder; the names come from the cited papers.
8. **Gated cards read from the rendered page, not the raw file at the revision.** Equality with the pin rests on the Hub API `sha` for `main` on the retrieval date.
9. **Licence column = the registered licence lines (scoring note l.18, `A_E3_REG_v2.json`), confirmed on each card.** Not checked: licences of upstream components, i.e. Mistral-7B-Instruct-v0.2 and the GPT-generated data in LLaVA-NeXT and SmolVLM2.
10. **"Parent COCO" note is beyond line 18.** Line 18 names COCO-vi, UIT-ViIC and XM3600 only. The plain-COCO finding is kept as a note inside the COCO-vi cell because the task brief asked for "COCO or its Vietnamese versions". The judge decides whether it stays in the printed row.
11. **Name variants checked.** The four cards, the four papers and the LLaVA-NeXT blog were text-searched for COCO, Crossmodal, XM3600 / XM-3600, XM100, "35L", UIT-ViIC and Vietnam. No hit names XM3600 or UIT-ViIC.
