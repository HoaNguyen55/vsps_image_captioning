# Retrieved or Random Examples? A Preregistered Controlled Study of Retrieval In-Context Captioning for Vietnamese

<!-- DRAFT 2 (CP-116 fixes), anonymous. Every number comes from number_manifest_C.tsv. No dataset caption appears anywhere in this draft. -->

## Abstract

In retrieval in-context captioning, a multimodal large language model sees the captions of training images similar to the query. We ask whether this helps Vietnamese captioning more than the same number of text-only captions drawn at random from the same in-domain memory, which separates retrieval from in-domain style.

We ran a preregistered study with Qwen2.5-VL-7B and InternVL3-8B. Each model's configuration was frozen on development data. It then passed a registered pooled one-look gate on a second development split (gate PASS); the registered object-guard hypothesis was not passed there. Each test set was looked at once.

On the OpenViIC test set (the 1,941 images left after removing 60 near-duplicates of the tuning set), retrieved examples beat random ones by +4.49 [3.52, 5.57] stripped CIDEr-D points, pooled over both models: P1 PASS (rule: point above +2.0, 95% CI above zero). The gain is carried mainly by Qwen2.5-VL (+8.33 [7.01, 9.76]) and was not detected for InternVL3 (+0.66 [−0.68, 1.99]). For both models, count-matched object precision against zero-shot stayed above the registered floor: +5.41 [3.88, 7.01] and +1.57 [0.65, 2.51] points.

On 2,500 Vietnamese XM3600 images, the gain was not detected out of domain: +0.70 [−0.45, 1.97], XM-a FAIL. The verified-precision part, XM-b, gave +0.59 [−0.31, 1.54]: PASS. The registered XM3600 prediction needs both parts, so it is not confirmed.

We release scores, image identifiers and hashes, but no captions.
