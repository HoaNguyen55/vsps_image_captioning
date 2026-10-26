## 1. Introduction

Open multimodal large language models (MLLMs) can caption images in Vietnamese with no task training. Their zero-shot captions still score far below fine-tuned systems on the Vietnamese benchmarks KTVIC [Pham2024KTVIC], UIT-OpenViIC [Bui2023OpenViIC] and the Vietnamese part of XM3600 [Thapliyal2022XM3600]. A companion study (anonymous submission B) shows that reference conventions, such as the absence of sentence-final punctuation in KTVIC references, move CIDEr-D [Vedantam2015CIDEr] substantially under Vietnamese scoring pipelines. Part of the zero-shot gap is therefore a matter of matching the references' conventions rather than of content.

**Retrieval in-context captioning** is a cheap way to close a style gap. For each query image, the captions of its nearest training images are put into the prompt as text examples, and the model is asked to write in the same way. Related work in English and in multilingual settings reports large CIDEr gains from retrieved or well-chosen examples [Yang2023ICLConfig; Ramos2023LMCap; Rebelo2025RSCap]. Studies of in-context configurations in English compare similarity-based selection with random selection, mostly for models that see the example images as well as their captions [Yang2023ICLConfig; Li2025UnveilingICL]. For Vietnamese with text-only example captions, the question remains which of two effects a gain over zero-shot prompting reflects:

- the effect of **retrieval**: examples that describe similar images;
- the effect of seeing **any in-domain captions**: examples that only show the dataset's style.

This study measures the first effect against the second. Our main control, `rand`, shows the model the same number k of captions from the same memory, chosen at random for each image. A second control, `fix`, shows one fixed set of k captions for every image. `zs` is plain zero-shot prompting. If retrieval helps only through style, `ret` and `rand` should score about the same.

We also track what retrieval may cost in faithfulness. Retrieved captions describe other images, and a model can copy their objects into its own caption [Li2024RetrievalRobustness]. We therefore registered a second prediction on **count-matched object precision** (anonymous companion submission A). It compares a caption's object mentions with those of the same model's zero-shot caption at an equal number of mentions, so that a longer caption is not penalised merely for naming more objects.

The study was preregistered in three stages, each committed before the data it uses reached the decoding machine:

1. exploration on development set A, which picks one configuration per model;
2. a one-look confirmation on development set B, with a registered gate;
3. a one-look test on each of two test sets.

The test registration fixed the estimands, the smallest effect size of interest (SESOI, +2.0 stripped CIDEr-D points), the decision rules, the wording each outcome allows, and the reporting of failures. We report every registered verdict as computed.

**Contributions.**
- A controlled comparison of retrieved, random, fixed and zero-shot examples for Vietnamese captioning with two open MLLMs, at each model's frozen configuration, preregistered in three stages with one look per test set.
- **In domain (OpenViIC test):** the registered primary is PASS, with the gain carried mainly by Qwen2.5-VL and not detected for InternVL3. Neither model loses count-matched object precision beyond the registered floor.
- **Out of domain (XM3600 Vietnamese):** the gain was not detected out of domain (XM-a FAIL), and the registered XM3600 prediction is not confirmed.
- A full record of the run: every registered row, every deviation and every exposure of test data. Scores, image ids and hashes are released; captions are not.

The paper does not propose a new method. Section 2 places the study among the closest work. Section 3 describes the method and the frozen configurations, and Section 4 the data and splits. Section 5 gives the registered analysis plan, Section 6 the results, and Section 7 the disclosures. Section 8 is reserved for the separately preregistered English arm, and Sections 9 and 10 give the limitations and conclusions.
