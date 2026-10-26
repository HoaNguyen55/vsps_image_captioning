# Retrieved or Random Examples? A Preregistered Controlled Study of Retrieval In-Context Captioning for Vietnamese

<!-- DRAFT 2 (CP-116 fixes), anonymous. Every number comes from number_manifest_C.tsv. No dataset caption appears anywhere in this draft. -->

## Abstract

In retrieval in-context captioning, a multimodal large language model sees the captions of training images similar to the query. We ask whether this helps Vietnamese captioning more than the same number of text-only captions drawn at random from the same in-domain memory, which separates retrieval from in-domain style.

We ran a preregistered study with Qwen2.5-VL-7B and InternVL3-8B. Each model's configuration was frozen on development data. It then passed a registered pooled one-look gate on a second development split (gate {{DF:ov_dev_b.gate.verdict|vw}}); the registered object-guard hypothesis was {{DF:ov_dev_b.H_G.passed|v:passed}} there. Each test set was looked at once.

On the OpenViIC test set (the {{PL:ov_test_primary1941.txt|i}} images left after removing {{PL:neardup60|i}} near-duplicates of the tuning set), retrieved examples beat random ones by {{OV:P1|e}} stripped CIDEr-D points, pooled over both models: P1 {{OV:P1.passed|v:pass}} (rule: point above +{{OV:SESOI|f1}}, 95% CI above zero). The gain is carried mainly by Qwen2.5-VL ({{OV:P1b.qwen25vl_7b|e}}) and was not detected for InternVL3 ({{OV:P1b.internvl3_8b|e}}). For both models, count-matched object precision against zero-shot stayed above the registered floor: {{OV:P2.qwen25vl_7b|e}} and {{OV:P2.internvl3_8b|e}} points.

On {{CHAIN:xm_staged|i}} Vietnamese XM3600 images, the gain was not detected out of domain: {{XM:XM_a|e}}, XM-a {{XM:XM_a.passed|v:pass}}. The verified-precision part, XM-b, gave {{XMB:XM_b|e}}: {{XMB:XM_b.passed|v:pass}}. The registered XM3600 prediction needs both parts, so it is {{XMB:XM_prediction|vw}}.

We release scores, image identifiers and hashes, but no captions.
