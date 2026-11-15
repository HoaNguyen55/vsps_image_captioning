> **PROVISIONAL.** Blind card of the conference draft v3.1 (`draft_v3_1/paper.md`, sha256 b42eecb1c8e574af98ade56902fae0676a440f6cfd579dd8690984be5ee6692d), written 2026-11-15. The draft text changes once more after 2026-11-16; this card is then refreshed from the new text before any scoring. Coordinator file: the scorer copy is everything from the line `## Paper card` down, with the JSON `id` replaced (see `SHUFFLE_KEY_DO_NOT_SHOW_SCORERS.md`). Every number below is copied from paper.md.

## Paper card

**Problem and stated limitation of prior work.** Open multimodal large language models (MLLMs) caption Vietnamese images without training, but far below fine-tuned systems. Retrieval in-context captioning puts the captions of similar memory images into the prompt. The paper states that a gain over zero-shot prompting may come from in-domain caption style rather than retrieval, and that the analyses testing this are in English or multilingual news captioning; as far as those papers state, none preregisters its contrasts, reports confidence intervals on the captioning score, or covers Vietnamese.

**Main claim.** In a preregistered test with one look per test set, retrieved example captions beat an equal number k of random captions from the same memory where memory and test set share a source, in Vietnamese and English, carried mainly by one of two models; outside the memory's source the registered predictions failed. The paper proposes no new method.

**Method / resource.** A measurement study with four prompt arms differing only in the example block: `ret` (the k most similar memory clusters by SigLIP2 cosine), `rand` (k clusters drawn per query, seeded), `fix` (one set per test set) and `zs` (zero-shot). Per model, k, example order, prompt tail and the threshold τ of an object-deletion step were frozen on development data in two registered stages; `rand` and `fix` run at the configuration picked on the `ret` score. Metrics: stripped CIDEr-D on word-segmented Vietnamese, PTB CIDEr-D in English, and a count-matched object precision against each model's zero-shot captions, gold taken from the references.

**Theorem, bound, identification result or provable property.** None.

**Data and splits (sizes).** Vietnamese memory: 10,501 images from KTVIC and UIT-OpenViIC training data, after a pre-specified filter excluded 2,056 of 12,557. Development: a KTVIC carve (size not printed), two halves of OpenViIC dev (911, 925), 500 XM3600 images. Tests: OpenViIC test, 1,941 of 2,001 images; 2,500 XM3600 Vietnamese images (600 set aside before the study, so no full-XM3600 result). English: memory from COCO Karpathy train and restval (112,255); COCO Karpathy test (5,000), NoCaps val (4,500). No training, no new annotation.

**Models and model families.** Qwen2.5-VL-7B-Instruct and InternVL3-8B, greedy, at most 60 new tokens; Qwen3-VL-8B-Instruct as verifier for the deletion step. Tests used 9.59 and 13.22 GPU-hours on one 24 GB GPU.

**Baselines and their years.** The controls `rand`, `fix` and `zs`. No other captioning method is run; a published fine-tuned score (75.58 CIDEr) is quoted as not comparable.

**Key numbers (`ret` − `rand`, 95% CI, as printed).** OpenViIC test, pooled: +4.49 [3.52, 5.57] (PASS); Qwen2.5-VL +8.33 [7.01, 9.76], InternVL3 +0.66 [−0.68, 1.99]. Object precision of `ret` against `zs`: +5.41 and +1.57 (PASS, floor −1.0). XM3600, pooled: +0.70 [−0.45, 1.97] (FAIL). COCO, pooled: +3.08 [2.08, 4.03] (PASS); InternVL3 −1.64 [−2.79, −0.49]. NoCaps: +1.73 [0.94, 2.50] (FAIL, point below +2.0). Pooled `ret` − `zs` on OpenViIC: +14.30. Qwen2.5-VL on OpenViIC: `ret` 39.81, `rand` 31.48, `zs` 20.05.

**Ablations, seeds, statistical tests, confidence intervals.** Paired image bootstrap (B = 2,000) for every row and per backbone; one primary test per language; other rows unadjusted; no p-values. The +2.0 threshold is a planning value with no recorded calibration, carried to English unchanged. One `rand` draw per image, one decode, no repeated runs. Development ablations and several registered secondary rows are named as not reported.

**Failure analysis.** The deletion step lowered InternVL3's CIDEr-D (33.62 against 39.50) and improved neither object measure. A post hoc near-copy check flags 12 of 1,941 queries. The NoCaps rows by domain label are named as not printed. No figure, no caption examples or error categories.

**Code/data release and licence statements.** Code, registrations, decision files and scores are available from the authors on request; no caption or per-image record is released. No licence is stated for the data sets.

**Positioning against closest prior work.** Two sentences set five analyses (2023–2026) that have a random control at equal shots or equal k, four on English caption data and one multilingual without Vietnamese, against this study; a search of their full texts found no registered one-look test and no CI on the captioning score. No comparison table and no head-to-head experiment.

**Out-of-domain or cross-language checks.** XM3600 Vietnamese, outside the memory's source (FAIL); an English arm with the frozen configurations (COCO PASS, NoCaps FAIL), registered after the Vietnamese verdicts, its NoCaps rule chosen after the XM3600 result.

**Stated limitations.** Two backbones; source match confounded with test set; reference-based metric, no human judgments; object gold limited to what references or labels name; one look, one random draw; batch composition; undisclosed model training data.

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
  "closest_work": ["OpenFlamingo (Awadalla et al.)", "MUNIChus (Chen et al.)", "In-context configuration study for captioning (Yang et al.)", "Retrieval robustness for retrieval-augmented captioning (Li et al.)", "Multimodal in-context learning analysis (Baldassini et al.)", "LMCap (Ramos et al.)", "Training-free multilingual remote-sensing captioning (Rebelo et al.)"]
}
```
