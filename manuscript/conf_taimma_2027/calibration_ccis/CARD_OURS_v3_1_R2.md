> **Rebuild 2 under CC-424 W2 (ruling 3 (i)-(ii)).** Blind card of the conference draft v3.1 (draft_v3_1/paper.md, sha256 b42eecb1c8e574af98ade56902fae0676a440f6cfd579dd8690984be5ee6692d), written 2026-11-15 from CARD_OURS_v3_1_PROVISIONAL.md (fce6012b) by removing the tells T-a, T-b and T-c only. Not yet the card of record: it is re-checked against the paper text of record after the page count (and after any cut k1-k3). Coordinator file: the scorer copy is everything from the line "## Paper card

**Problem and stated limitation of prior work.** Open multimodal LLMs caption Vietnamese images without training, far below fine-tuned systems. Retrieval in-context captioning prompts them with captions of similar memory images; a gain over zero-shot may come from in-domain caption style, not retrieval. Analyses of this are in English or in multilingual news captioning; as far as they state, none preregisters its contrasts, reports CIs on the captioning score, or covers Vietnamese.

**Main claim.** In a preregistered one-look test, retrieved example captions beat an equal number of random ones from the same memory where memory and test set share a source, in Vietnamese and English, carried mainly by one of two models; outside that source the registered predictions failed. No new method is proposed.

**Method / resource.** Four prompt arms differing only in the example block: ret (k most similar memory clusters, SigLIP2 cosine), rand (k random clusters per query), fix (one set per test set), zs (zero-shot). Per model, k, example order, prompt tail and an object-deletion threshold τ were frozen in two registered development stages; rand and fix run at the configuration picked on the ret score. Metrics: stripped CIDEr-D (Vietnamese), PTB CIDEr-D (English), count-matched object precision against each model's zero-shot captions, gold from references.

**Theorem, bound, identification result or provable property.** None.

**Data and splits (sizes).** Vietnamese memory: 10,501 KTVIC and UIT-OpenViIC training images (filter excluded 2,056 of 12,557). Development: KTVIC carve (size not printed), OpenViIC dev halves (911, 925), 500 XM3600 images. Tests: OpenViIC test, 1,941 of 2,001; 2,500 XM3600 Vietnamese images (600 set aside, so no full-XM3600 result). English: COCO Karpathy train+restval memory (112,255); COCO Karpathy test (5,000), NoCaps val (4,500). No training, no new annotation.

**Models and model families.** Qwen2.5-VL-7B-Instruct and InternVL3-8B, greedy, at most 60 new tokens; Qwen3-VL-8B-Instruct verifies the deletion step. Tests: 9.59 and 13.22 GPU-hours, one 24 GB GPU.

**Baselines and their years.** Controls rand, fix and zs; no other captioning method run. A published fine-tuned 75.58 CIDEr is quoted as not comparable.

**Key numbers (ret − rand, 95% CI, as printed).** OpenViIC test, pooled: +4.49 [3.52, 5.57] (PASS); InternVL3 +0.66 [−0.68, 1.99]. Object precision, ret against zs: +5.41 and +1.57 (PASS, floor −1.0). XM3600, pooled: +0.70 [−0.45, 1.97] (FAIL). COCO, pooled: +3.08 [2.08, 4.03] (PASS); InternVL3 −1.64 [−2.79, −0.49]. NoCaps: +1.73 [0.94, 2.50] (FAIL, point below +2.0).

**Ablations, seeds, statistical tests, confidence intervals.** Paired image bootstrap (B = 2,000), every row and per backbone; one primary test per language, other rows unadjusted, no p-values. The +2.0 threshold is a planning value without recorded calibration, carried unchanged to English. One rand draw and one decode per image. Development ablations and several registered secondaries are not reported.

**Failure analysis.** The deletion step lowered InternVL3's CIDEr-D (33.62 against 39.50) and improved neither object measure. A post hoc near-copy check flags 12 of 1,941 queries. NoCaps rows by domain label are not printed. No figure, caption examples or error categories.

**Code/data release and licence statements.** Code, registrations, decision files and scores on request; no caption or per-image record is released. No data-set licence stated.

**Positioning against closest prior work.** Two sentences set this study against five analyses (2023–2026) with an equal-k or equal-shot random control (four English, one multilingual without Vietnamese); a full-text search found none with a registered one-look test or a CI on the captioning score. No comparison table, no head-to-head experiment.

**Out-of-domain or cross-language checks.** XM3600 Vietnamese, outside the memory's source (FAIL); English arm, frozen configurations (COCO PASS, NoCaps FAIL), registered after the Vietnamese verdicts, NoCaps rule chosen after XM3600.

**Stated limitations.** Two backbones; source match confounded with test set; reference-based metric, no human judgments; object gold limited to references and labels; one look, one random draw; batch composition; undisclosed training data.

## Direction card

```json
{
  "id": "OURS",
  "title": "A preregistered comparison of retrieved and random in-prompt example captions for training-free Vietnamese image captioning",
  "gap": "Gains of retrieval in-context captioning over zero-shot prompting may come from in-domain caption style rather than retrieval; analyses with a random-example control exist for English and multilingual news captioning, but none covers Vietnamese, preregisters its contrasts or reports confidence intervals on the captioning score.",
  "novelty_claim": "The study will compare retrieved example captions with an equal number of random captions from the same memory, beside fixed-example and zero-shot controls, for two open multimodal models reported separately, with configurations frozen on development data and one registered look per test set, in and outside the memory's source, in Vietnamese and English.",
  "application": "Guidance for training-free captioning in low-resource languages: whether a retrieval index beats random in-domain examples, and which controls a retrieval gain needs before it is credited.",
  "data": "A Vietnamese memory of 10,501 images from KTVIC and UIT-OpenViIC training data; OpenViIC test and 2,500 XM3600 Vietnamese images as test sets; an English memory from COCO Karpathy train with COCO Karpathy test and NoCaps val. No training and no new annotation.",
  "method": "Cluster the memory by a visual-similarity rule and retrieve by SigLIP2 cosine; prompt Qwen2.5-VL-7B and InternVL3-8B with retrieved, random, fixed or no example captions as text; freeze configurations in two registered development stages; score stripped CIDEr-D and count-matched object precision with paired image bootstrap CIs, and decide each registered prediction once.",
  "kill_pilot": "On a held-out half of the OpenViIC development set, compare retrieved with random examples at the frozen configurations; the direction fails unless the pooled difference has a CI above zero and a point of at least +4.0 stripped CIDEr-D points.",
  "target_year": 2027,
  "venue": "international conference",
  "closest_work": ["OpenFlamingo (Awadalla et al.)", "MUNIChus (Chen et al.)", "In-context configuration study for captioning (Yang et al.)", "Retrieval robustness for retrieval-augmented captioning (Li et al.)", "Multimodal in-context learning analysis (Baldassini et al.)", "LMCap (Ramos et al.)"]
}
```
