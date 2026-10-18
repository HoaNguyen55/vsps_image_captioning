# Pre-registration addendum: E1 K2 seed placebo (two sampling seeds of LLaVA-1.5-7B on CHAIR-500)

**Frozen:** 2026-10-18. **This addendum was committed before any K2 output existed.** K2 is job 5 of the M2 queue. When this file was written, M2 was running queue job 1 (61_p1_3b_s42, started 08:50:41Z per `M2_EVENTS.log`) and no K2 job had started. The A-verifier checks the commit time against the `created_utc` and mtime of the first K2 output.
**Parent registration:** `manuscript/research_r10/E1/REPORT.txt` §1 H4 and §4 K2 (commit 6c647a6). It defines the placebo as two sampling seeds of one model and fixes the prediction and the kill rule, but no sampling settings. This addendum fixes only what §4 leaves open; nothing in §4 is changed.
**Companion:** `2026-10-18_n9_count_matched_leaderboard.md`, which uses the K2 result to choose N9's primary count control (D17 §3(c)4; H6 P5). Machine-readable values are in `2026-10-18_n9_count_matched_leaderboard.json` (key `k2_addendum`).

## 1. What runs

- **Model:** the N9 base, `liuhaotian/llava-v1.5-7b@4481d270cc22fd5c4d1bb5df129622006ccd9234` with the vision tower `openai/clip-vit-large-patch14-336@ce19dc912ca5cd21c8a653c79e251e808ccabcd1`, loaded by `scripts/lvlm/decode_llava.py` (sha256 `522bfc1694e21d85ec8335d1ce6e3d9ee401c671da7fc304ec8b4d48c3063561`, committed with this file). The harness rebuilds the LLaVA-1.5 `model_vqa.py` inference path; see the N9 prereg §2.
- **Images:** `data/coco_probe/chair500_ids.txt` (sha256 `00c8458c9fbb19c6f21fcfb82cdac617842c0570e874e1540b19f52fab70f6ee`): the 500 COCO val2014 ids of LiM's `chair-500.jsonl` at `yuezih/less-is-more@f26e187aadacc49a7cfc30443f0e9bae865b8e2e` (source sha256 `d4002b206d2439d96c5955172551ee1129e179f17898f7248b8743ee98dbe32a`), with provenance in `data/coco_probe/chair500_ids.provenance.json`. 495 of them have instance annotations; the scorer drops the others, as E1 and CHAIR do.
- **Prompt:** the LLaVA `llava_v1` conversation with the chair-500 question "Please describe this image in detail."
- **Sampling:** temperature 1.0, top-p 1.0, top-k 0 (off), so each run samples from the model's own distribution and the two runs are exchangeable draws of one system. No other setting is tried.
- **Seeds:** 1 and 2. The harness seeds each batch with `torch.manual_seed(seed * 1000003 + index of the batch's first image)`, so a resumed run repeats the same draws.
- **Length and batching:** `max_new_tokens` 512, one beam, fp16, batch size 8 (the N9 batch size; if 8 does not fit, both K2 runs and all N9 runs use 4).
- **Commands** (`$IMG` = folder of the COCO val2014 images, `$OUT` = output folder):

```
python3 scripts/lvlm/decode_llava.py \
    --label k2_seed1 \
    --out $OUT/k2_seed1.json \
    --image-ids data/coco_probe/chair500_ids.txt \
    --image-dir $IMG \
    --base liuhaotian/llava-v1.5-7b@4481d270cc22fd5c4d1bb5df129622006ccd9234 \
    --vision openai/clip-vit-large-patch14-336@ce19dc912ca5cd21c8a653c79e251e808ccabcd1 \
    --do-sample --temperature 1.0 --top-p 1.0 --top-k 0 --seed 1 \
    --max-new-tokens 512 \
    --batch-size 8

python3 scripts/lvlm/decode_llava.py \
    --label k2_seed2 \
    --out $OUT/k2_seed2.json \
    --image-ids data/coco_probe/chair500_ids.txt \
    --image-dir $IMG \
    --base liuhaotian/llava-v1.5-7b@4481d270cc22fd5c4d1bb5df129622006ccd9234 \
    --vision openai/clip-vit-large-patch14-336@ce19dc912ca5cd21c8a653c79e251e808ccabcd1 \
    --do-sample --temperature 1.0 --top-p 1.0 --top-k 0 --seed 2 \
    --max-new-tokens 512 \
    --batch-size 8
```

## 2. Comparison

- X = seed 2, B = seed 1, scored on the 495 images with instance annotations.
- **Scorer:** `scripts/lvlm/e1_chair_count.py` (sha256 `1e59ff12100b4d489f92b88045ef99bee1f8c36045e449c37e282504653213b4`), a byte-identical copy of E1's scorer, which reproduces E1's `e1_results.json` byte for byte (check: `.session_backup/2026-10-18/paperA_tasks/P1/e1_scorer_repro_check.json`). Gold = CHAIR gold from `annotations_trainval2014.zip` (sha256 `031296bbc80c45a1d1f76bf9a90ead27e94e99ec629208449507a4917a3bf009`) with `data/coco_probe/chair_synonyms.txt` (sha256 `b685537b36fe21b791c87151b96a991ceb582edff19f3da204dcc7a7905502f2`).
- **Statistic:** dP_MCP = E1 `compare()` `dP_matched_prefix`, the class-level precision of the first k* = min(k_X, k_B) distinct COCO classes of each caption, X minus B. A paired image bootstrap with 2,000 resamples and seed 0 (E1 §4) gives the 95% percentile interval.
- The same two runs also give the sentence tie-average and the uniform random-subset differences at the same k* (definitions in the N9 prereg §4), which the N9 control-selection rule needs.

## 3. Frozen prediction and kill rule (E1 §1 H4 and §4 K2, restated)

- **Prediction:** |dP_MCP| < 0.5.
- **Kill rule:** |dP_MCP| > 1.0, or a 95% interval that excludes 0, means the matched-prefix control is miscalibrated: stop, and draw no matched-prefix conclusion from E1 or N9 (E1 §4 K2).
- **The other two controls:** a control with |dP| > 1.0 or an interval excluding 0 is dropped from the specification curve (Paper A §6.3 (i)).
- **Primary-control selection for N9** (D17 §3(c)4, H6 P5): a control is *admissible* iff |dP| ≤ 0.5 and its 95% interval covers 0. N9's primary control C* is the first admissible control in the order matched prefix, sentence tie-average, uniform random subset. Because the matched prefix comes first, it stays primary whenever it is admissible, as H6 P5 requires when several qualify. If no control is admissible, N9 has no primary per-image control (N9 prereg §7, K-placebo).
- **Labels**, all computed by these rules from the K2 statistics: `K2_PREDICTION` = HELD / NOT_HELD; per control, `KILL` = FIRED / NOT_FIRED and `ADMISSIBLE` = true / false; `C_STAR` = the selected control or NONE.

## 4. Reporting

The result is reported whichever way it falls, in Paper A §6.3 (Table 6.1, seed-placebo row). K2 does not depend on any N9 output.
