# Pre-registration: N9, a count-matched leaderboard of public LLaVA-1.5-7B anti-hallucination training checkpoints on CHAIR-500

**Registered before any N9 output exists.** Frozen 2026-10-18. The M2 operator starts N9 only after this file is committed.
**Mandate:** R11_FOR_GEMINI §D (N9); PD-3 Q4; PD-4 Q6; PD-6 Q1(a), Q3 and Q4(c); D17 §3(c)4 and binding condition 4; PD-9 Q6. Paper A owns N9 (PD-6 ledger); it uses no KTVIC data.
**Predictions:** `manuscript/research_r11/L6/REPORT.txt` §3 D1, with the kill rules of §6.
**Machine-readable:** `2026-10-18_n9_count_matched_leaderboard.json` (frozen predictions, thresholds, pins, and every comparator value with its source path, key and sha256).
**Companion:** `2026-10-18_e1_k2_placebo_addendum.md`. K2 runs first, and its result selects N9's primary count control (§5).
**Committed with this file:** `scripts/lvlm/decode_llava.py` (sha256 `522bfc1694e21d85ec8335d1ce6e3d9ee401c671da7fc304ec8b4d48c3063561`), `scripts/lvlm/e1_chair_count.py` (sha256 `1e59ff12100b4d489f92b88045ef99bee1f8c36045e449c37e282504653213b4`), `data/coco_probe/chair500_ids.txt` (sha256 `00c8458c9fbb19c6f21fcfb82cdac617842c0570e874e1540b19f52fab70f6ee`) and its provenance JSON.

## 1. Checkpoints

Every repo id, commit and licence below was read from the Hugging Face model API and model card, and from the official GitHub repository, on 2026-10-18 (evidence: `.session_backup/2026-10-18/paperA_tasks/P1/evidence/`). Every run is pinned to the commit shown.

| Run | Method | `--base` | `--lora` (in order) | Vision LoRA | Licence (source) |
|---|---|---|---|---|---|
| `n9_base` (comparator) | LLaVA-1.5-7B (base) | `liuhaotian/llava-v1.5-7b@4481d270cc22fd5c4d1bb5df129622006ccd9234` | — | — | Llama 2 Community License (model card README, "License" section) |
| `n9_povid` (method) | POVID | `liuhaotian/llava-v1.5-7b@4481d270cc22fd5c4d1bb5df129622006ccd9234` | `YiyangAiLab/llava_POVID_stage_one_lora@d6c79d54be16246404f910a4453eb64b8b31af25`<br>`YiyangAiLab/llava_POVID_stage_two_lora@bdb48949e04cf7605a606b7159726ac161f96b25` | not applied (`--drop-vision-lora`; authors' path) | Llama 2 Community License (model card README, "License" section); Apache-2.0 (repository LICENSE (README links the HF models; card states none)) |
| `n9_rlaifv` (method) | RLAIF-V | `openbmb/RLAIF-V-7B@90e8e7338297c7ee753ae706b1571d46225c5c19` | — | — | apache-2.0 (model card license field; the repository README restricts use to research) |
| `n9_chairdpo` (method) | CHAIR-DPO | `aimagelab/CHAIR-DPO_LLaVA-1.5-7B@bd9ab77aa0f9183ad1a30e4cc8cecc2cd2b175b8` | — | — | apache-2.0 (model card license field) |
| `n9_sentinel` (method) | SENTINEL | `liuhaotian/llava-v1.5-7b@4481d270cc22fd5c4d1bb5df129622006ccd9234` | `psp-dada/LLaVA-v1.5-7B-SENTINEL@016b6dced6c24bd26b3736a8cab23ea874dca7c7` | applied if present | Llama 2 Community License (model card README, "License" section); apache-2.0 (model card license field and repository LICENSE) |
| `n9_hadpo` (method) | HA-DPO | `liuhaotian/llava-v1.5-7b@4481d270cc22fd5c4d1bb5df129622006ccd9234` | `juliozhao/hadpo-llava-1.5@72b1bcf8d86e60937e1df1ca1386d1c97bf95eb1` | applied if present | Llama 2 Community License (model card README, "License" section); Apache-2.0 (repository LICENSE (README links the HF models; card states none)) |
| `n9_opadpo` (method) | OPA-DPO | `liuhaotian/llava-v1.5-7b@4481d270cc22fd5c4d1bb5df129622006ccd9234` | `zhyang2226/opadpo-lora_llava-v1.5-7b@f589492241ddfaf195cdedd20781edfa8d072717` | applied if present | Llama 2 Community License (model card README, "License" section); MIT (repository LICENSE (card states none)) |
| `n9_povid_fullmerge` (sensitivity) | POVID, full merge (sensitivity) | `liuhaotian/llava-v1.5-7b@4481d270cc22fd5c4d1bb5df129622006ccd9234` | `YiyangAiLab/llava_POVID_stage_one_lora@d6c79d54be16246404f910a4453eb64b8b31af25`<br>`YiyangAiLab/llava_POVID_stage_two_lora@bdb48949e04cf7605a606b7159726ac161f96b25` | applied if present | Llama 2 Community License (model card README, "License" section); Apache-2.0 (repository LICENSE (README links the HF models; card states none)) |
| all runs | CLIP vision tower | `--vision openai/clip-vit-large-patch14-336@ce19dc912ca5cd21c8a653c79e251e808ccabcd1` | | | MIT (official repository openai/CLIP LICENSE (HF card states none); card: research output) |

**Licence rule ("open only").** A checkpoint is used only if its weights are public on Hugging Face without gating and the authors give an explicit licence or use statement, on the model card or in the official repository, that permits research use. Each licence is recorded as found. All checkpoints are LLaVA-1.5 derivatives, so the Llama 2 Community License of the base also applies. Outputs are used for evaluation only; no weights are redistributed.

**Excluded, with reasons:**
- **HALVA** (`pritamqu/halva7b-lora@9b96dbf31c5622157fbb90136dacf619addaf3c6`): no licence statement: HF card has no licence, GitHub pritamqu/HALVA has no LICENSE file (API licence null) and its README states none; dropped under the CapArena rule (licence_check_2026-10-15.json). Consequence: prediction (c) is not testable; revivable only by a committed addendum before any HALVA output.
- **HSA-DPO**: the only released model is a LLaVA-v1.5-13B LoRA on ModelScope (xiaowenyi/HSA-DPO); no 7B, no HF release. Consequence: chosen-fewer group of (b) = HA-DPO, SENTINEL.
- **mDPO**: no LLaVA-1.5-7B checkpoint released (README: preference data and a Bunny trainer only). Consequence: near-balanced group of (b) = POVID.

**Loading rule: each method is decoded as its authors' own inference path builds it.**
- Full checkpoints (RLAIF-V, CHAIR-DPO) replace the base's language model and projector. Vision-tower weights saved inside them are not used, because the LLaVA builder ignores them too; the harness records their maximum absolute difference from the CLIP tower.
- LoRA checkpoints are merged on top of the base. `non_lora_trainables.bin` is loaded first, then every LoRA pair is merged as W + (lora_alpha / r) B A.
- Adapters with **vision-tower LoRA** (header scan of the released files):
  - **OPA-DPO.** Its model card says the LoRA modules sit on the vision tower too and must be loaded on it, so they are merged.
  - **POVID** (both stages). Its own `povid_infer.py` loads the base with the vision tower delay-loaded, so PeftModel never sees those modules and they are not applied. N9 therefore decodes POVID with `--drop-vision-lora` (primary).
  - **POVID full merge** (`n9_povid_fullmerge`) is a registered sensitivity run: it is reported next to POVID and never enters a verdict.
- **Expected merged LoRA modules** (from the adapters' own tensor names; P1 dry run `dry_run_loader.json`). Each output's `model.lora_merged` must match these counts:

| Run | LoRA | merged modules by component | skipped | non_lora tensors |
|---|---|---|---|---|
| `n9_povid` | `YiyangAiLab/llava_POVID_stage_one_lora` | {"language_model": 64} | {"vision": 48} | 0 |
| `n9_povid` | `YiyangAiLab/llava_POVID_stage_two_lora` | {"language_model": 224} | {"vision": 72} | 0 |
| `n9_sentinel` | `psp-dada/LLaVA-v1.5-7B-SENTINEL` | {"language_model": 224} | — | 4 |
| `n9_hadpo` | `juliozhao/hadpo-llava-1.5` | {"language_model": 224} | — | 4 |
| `n9_opadpo` | `zhyang2226/opadpo-lora_llava-v1.5-7b` | {"language_model": 224, "vision": 144, "projector": 2} | — | 0 |
| `n9_povid_fullmerge` | `YiyangAiLab/llava_POVID_stage_one_lora` | {"language_model": 64, "vision": 48} | — | 0 |
| `n9_povid_fullmerge` | `YiyangAiLab/llava_POVID_stage_two_lora` | {"language_model": 224, "vision": 72} | — | 0 |

## 2. Decoding (identical for every run)

- **Harness.** `scripts/lvlm/decode_llava.py` rebuilds the original LLaVA-1.5 inference path (`llava/eval/model_vqa.py` as used by LiM's CHAIR evaluation):
  - conversation template `llava_v1`, with the question "Please describe this image in detail.", which is the chair-500 question;
  - LLaVA's `tokenizer_image_token` with the slow Llama tokenizer;
  - image preprocessing `pad` (expand to a square with the CLIP mean colour, then the CLIP processor);
  - the CLIP layer −2 patch features and the `mlp2x_gelu` projector;
  - `skip_special_tokens` decoding, then strip.
  The model is transformers' `LlavaForConditionalGeneration`. Its tensor set, built from the base and CLIP configs, equals the 686 tensors of the official `llava-hf/llava-1.5-7b-hf` port (P1 dry run).
- **Settings.** Greedy decoding (no sampling), one beam, `max_new_tokens` 512, fp16, batch size 8 for every run. If batch 8 does not fit on the base run, every N9 and K2 run uses 4. The extra HF vocabulary rows (ids 32000 to 32063) are suppressed, so only the original 32,000-token vocabulary can be generated.
- **Prompt.** The prompt token ids are identical under transformers 4.37.2 (LLaVA's pinned version) and 4.51.3 (M2), and for the tokenizers of the base, RLAIF-V and CHAIR-DPO, which share one `tokenizer.model` (sha256 `9e556afd44213b6bd1be2b850ebbbd98f5481437a8021afaf58ee7fb1818d347`; check in `evidence/tokenizer/`). Each output records `prompt_template_ids_sha256`.
- **CPU self-test.** `python3 scripts/lvlm/decode_llava.py --selftest` covers the argument, prompt, key-map, LoRA, coverage and output-schema checks. With torch and transformers installed it also runs a tiny random LLaVA end to end, in which batched greedy decoding equals batch size 1 and seeded sampling repeats after a resume. The operator runs it once on M2 before the first job.
- **Commands** (`$IMG` = folder of the COCO val2014 images, `$OUT` = output folder; run the K2 pair of the companion addendum first):

```
python3 scripts/lvlm/decode_llava.py \
    --label n9_base \
    --out $OUT/n9_base.json \
    --image-ids data/coco_probe/chair500_ids.txt \
    --image-dir $IMG \
    --base liuhaotian/llava-v1.5-7b@4481d270cc22fd5c4d1bb5df129622006ccd9234 \
    --vision openai/clip-vit-large-patch14-336@ce19dc912ca5cd21c8a653c79e251e808ccabcd1 \
    --max-new-tokens 512 \
    --batch-size 8

python3 scripts/lvlm/decode_llava.py \
    --label n9_povid \
    --out $OUT/n9_povid.json \
    --image-ids data/coco_probe/chair500_ids.txt \
    --image-dir $IMG \
    --base liuhaotian/llava-v1.5-7b@4481d270cc22fd5c4d1bb5df129622006ccd9234 \
    --vision openai/clip-vit-large-patch14-336@ce19dc912ca5cd21c8a653c79e251e808ccabcd1 \
    --lora YiyangAiLab/llava_POVID_stage_one_lora@d6c79d54be16246404f910a4453eb64b8b31af25 \
    --lora YiyangAiLab/llava_POVID_stage_two_lora@bdb48949e04cf7605a606b7159726ac161f96b25 \
    --drop-vision-lora \
    --max-new-tokens 512 \
    --batch-size 8

python3 scripts/lvlm/decode_llava.py \
    --label n9_rlaifv \
    --out $OUT/n9_rlaifv.json \
    --image-ids data/coco_probe/chair500_ids.txt \
    --image-dir $IMG \
    --base openbmb/RLAIF-V-7B@90e8e7338297c7ee753ae706b1571d46225c5c19 \
    --vision openai/clip-vit-large-patch14-336@ce19dc912ca5cd21c8a653c79e251e808ccabcd1 \
    --max-new-tokens 512 \
    --batch-size 8

python3 scripts/lvlm/decode_llava.py \
    --label n9_chairdpo \
    --out $OUT/n9_chairdpo.json \
    --image-ids data/coco_probe/chair500_ids.txt \
    --image-dir $IMG \
    --base aimagelab/CHAIR-DPO_LLaVA-1.5-7B@bd9ab77aa0f9183ad1a30e4cc8cecc2cd2b175b8 \
    --vision openai/clip-vit-large-patch14-336@ce19dc912ca5cd21c8a653c79e251e808ccabcd1 \
    --max-new-tokens 512 \
    --batch-size 8

python3 scripts/lvlm/decode_llava.py \
    --label n9_sentinel \
    --out $OUT/n9_sentinel.json \
    --image-ids data/coco_probe/chair500_ids.txt \
    --image-dir $IMG \
    --base liuhaotian/llava-v1.5-7b@4481d270cc22fd5c4d1bb5df129622006ccd9234 \
    --vision openai/clip-vit-large-patch14-336@ce19dc912ca5cd21c8a653c79e251e808ccabcd1 \
    --lora psp-dada/LLaVA-v1.5-7B-SENTINEL@016b6dced6c24bd26b3736a8cab23ea874dca7c7 \
    --max-new-tokens 512 \
    --batch-size 8

python3 scripts/lvlm/decode_llava.py \
    --label n9_hadpo \
    --out $OUT/n9_hadpo.json \
    --image-ids data/coco_probe/chair500_ids.txt \
    --image-dir $IMG \
    --base liuhaotian/llava-v1.5-7b@4481d270cc22fd5c4d1bb5df129622006ccd9234 \
    --vision openai/clip-vit-large-patch14-336@ce19dc912ca5cd21c8a653c79e251e808ccabcd1 \
    --lora juliozhao/hadpo-llava-1.5@72b1bcf8d86e60937e1df1ca1386d1c97bf95eb1 \
    --max-new-tokens 512 \
    --batch-size 8

python3 scripts/lvlm/decode_llava.py \
    --label n9_opadpo \
    --out $OUT/n9_opadpo.json \
    --image-ids data/coco_probe/chair500_ids.txt \
    --image-dir $IMG \
    --base liuhaotian/llava-v1.5-7b@4481d270cc22fd5c4d1bb5df129622006ccd9234 \
    --vision openai/clip-vit-large-patch14-336@ce19dc912ca5cd21c8a653c79e251e808ccabcd1 \
    --lora zhyang2226/opadpo-lora_llava-v1.5-7b@f589492241ddfaf195cdedd20781edfa8d072717 \
    --max-new-tokens 512 \
    --batch-size 8

python3 scripts/lvlm/decode_llava.py \
    --label n9_povid_fullmerge \
    --out $OUT/n9_povid_fullmerge.json \
    --image-ids data/coco_probe/chair500_ids.txt \
    --image-dir $IMG \
    --base liuhaotian/llava-v1.5-7b@4481d270cc22fd5c4d1bb5df129622006ccd9234 \
    --vision openai/clip-vit-large-patch14-336@ce19dc912ca5cd21c8a653c79e251e808ccabcd1 \
    --lora YiyangAiLab/llava_POVID_stage_one_lora@d6c79d54be16246404f910a4453eb64b8b31af25 \
    --lora YiyangAiLab/llava_POVID_stage_two_lora@bdb48949e04cf7605a606b7159726ac161f96b25 \
    --max-new-tokens 512 \
    --batch-size 8
```

## 3. Images

- **Id list.** `data/coco_probe/chair500_ids.txt` (sha256 `00c8458c9fbb19c6f21fcfb82cdac617842c0570e874e1540b19f52fab70f6ee`) holds the 500 COCO ids of LiM's `CHAIR-eval/data/chair-500.jsonl` at `yuezih/less-is-more@f26e187aadacc49a7cfc30443f0e9bae865b8e2e` (sha256 `d4002b206d2439d96c5955172551ee1129e179f17898f7248b8743ee98dbe32a`, Apache-2.0), in file order.
- **Provenance and use.** The ids are randomly sampled from COCO val2014 with seed 0 (LiM README). HALVA uses the same list, and so do the released LiM outputs that E1 re-scored.
- **Checks.**
  - All 500 ids are in COCO val2014.
  - 495 have instance annotations. The other 5 are decoded but not scored, as in E1 and CHAIR.
- **Image files.** COCO val2014 files (`COCO_val2014_%012d.jpg`, from `http://images.cocodataset.org/val2014/`, or the same bytes under `%012d.jpg`). Every output records the sha256 of every image; the analysis requires identical image bytes in every run (§7, K-protocol).

## 4. Scoring

- **Scorer.** `scripts/lvlm/e1_chair_count.py` (sha256 `1e59ff12100b4d489f92b88045ef99bee1f8c36045e449c37e282504653213b4`). It is the unchanged E1 scorer (CHAIR rules, COCO-80, synonyms), and it reproduces E1's `e1_results.json` byte for byte from the pinned E1 inputs (`e1_scorer_repro_check.json`). It is also the file that the 7254a39 preregs pin by the same sha256.
- **Gold.** CHAIR gold (val2014 instance labels plus the five reference captions, through the synonym list), from `annotations_trainval2014.zip` (sha256 `031296bbc80c45a1d1f76bf9a90ead27e94e99ec629208449507a4917a3bf009`) and `data/coco_probe/chair_synonyms.txt` (sha256 `b685537b36fe21b791c87151b96a991ceb582edff19f3da204dcc7a7905502f2`).
- **Per run.** E1 `agg()`: CHAIR_s, CHAIR_i, Recall, M (distinct classes per caption), TP, class precision P, F1 and words per caption.
- **Per method j vs the base** (k* = min(k_j, k_base) per image):
  - dP_raw and dR_raw (E1 `compare()`);
  - **dP_MCP**, the matched prefix (E1 `compare()` `dP_matched_prefix`): precision of the first k* distinct classes of each caption;
  - **dP_sent**, the sentence tie-average at k*. Captions are split into sentences on `[.!?]+`. The k* classes are taken in sentence order, and the boundary sentence's new classes are tie-averaged. This is the reference implementation `sent_tie_avg_tp` / `per_image_ext` of `.session_backup/2026-10-13/r10_cpu/run_e1_x1pb.py` (sha256 `047d167cdaed8ada4c71b766586a46ff2c2507dc0572793a30d38b015fe8f6fa`);
  - **dP_rand**, the uniform random subset at k*, as the exact expectation k*·TP/M per caption;
  - **dP_TRF**, the precision residual at the method's own mean count on the base's truncation frontier: E1 `trunc_curve` (K = 12, prefix order) and `interp_loglog`, giving 100·(TP_j − TP̂_base(M_j)) / M_j. If M_j is at or above the frontier's top point, dP_TRF is "not computable" (E1 returns NaN);
  - **Δm** = M_j − M_base (classes per caption);
  - **CAR** in its single-caption form, as in E1's `decomposition_prefix`. The ranking source is the base's own order of mention, so the base re-rank term D is 0. The terms are count C = dP_raw − dP_TRF, allocation B = dP_TRF − dP_C* and choice A = dP_C*. They telescope to dP_raw. Shapley averaging does not apply, because single captions allow only this order. The mean count at each vertex (M_base, M_j and the mean k*) is reported.
- **Statistics.**
  - Paired bootstrap over the scored images: 5000 resamples, seed 0, with the same image draws for every run, so that differences between checkpoints have valid intervals. 95% percentile intervals.
  - Two-sided bootstrap p-values with the +1 correction, as in `run_e1_x1pb.two_sided_boot_p`.
  - Holm correction over the six method-vs-base comparisons, separately for each endpoint.

## 5. Primary endpoints (PD-2 Q1: the count-matched comparison is primary, one endpoint per claim)

- **P1 (object choice; the leaderboard's count-controlled column).** dP under the control C* at per-image matched count k*.
  - **Choice of C*.** The K2 rule of the companion addendum: the first admissible control (|dP| ≤ 0.5 and 95% interval covering 0 on the seed placebo) in the order matched prefix, sentence tie-average, uniform random subset.
  - **Verdict.** A method **SURVIVES** iff its Holm-adjusted p < 0.05 AND dP_C* ≥ +1.0 (E1 §4 SESOI). The other two controls go to the specification curve.
- **P2 (frontier; PD-2's training-time endpoint).** dP_TRF, the residual at the method's own count on the base's frontier. The base's own residual is 0, so the paired change against the comparator is dP_TRF itself.
  - **Verdict.** A method is **OFF_FRONTIER** iff its Holm-adjusted p < 0.05 AND dP_TRF ≥ +1.0.
  - PD-2's KTVIC curve (b = 0.7468) belongs to another dataset and backbone. For N9, the registered curve is therefore the base's own truncation frontier, built by the rule above from the base run.
- **Never the headline** (PD-2): raw dP and dR, CHAIR_s, CHAIR_i, M and words per caption. They are always reported next to P1 and P2.

## 6. Frozen predictions (L6 §3 D1, with numeric thresholds)

- **(a) Training beats decoding at matched count (E1-H3).**
  - **Statistic.** The median over the six methods of dP_C* is compared with E1's mean over its 15 decoding comparisons under the same control. That mean is read in code from `.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json` (sha256 `184f9ccac1b9a930e4b0f75d68d05fba43f41d855c76494eb3ebf58aa69c3591`): matched prefix 0.621 (`overview_15_pairs.mean_dP_MCP_prefix`); sentence tie average 0.652 (`overview_15_pairs.mean_dP_MCP_sent_tieavg`); uniform random subset 2.764 (`overview_15_pairs.mean_dP_MCP_rand_exact`).
  - **Verdict.** HELD if the median exceeds the comparator and the bootstrap 95% lower bound of the median also exceeds it. POINT_ONLY if only the point estimate exceeds it. NOT_HELD otherwise.
  - **Descriptive.** E1-H3's own form, median against median: the median of E1's 15 matched-prefix decoding estimates is 0.427 (computed from `pairs_15.*.dP_MCP_prefix.est`).
- **(b) The count sign of the training data orders the count shift. This is the primary frozen prediction.**
  - **Groups.** They are named as in L6 and restricted to released checkpoints. Chosen-fewer: HA-DPO and SENTINEL (HSA-DPO has no 7B release). Near-balanced: POVID (mDPO has no checkpoint).
  - **Their training-data mean Δk,** read in code from `.session_backup/2026-10-14/r11_verify/c6_n3_rlaifv_rlhfv_audit.json` (sha256 `5d572461d17412a9ebb061276d870bff9bb36871b7381b0440d297983c682d49`, `summary_table_7_datasets.*.mean_dk`): HA-DPO -0.691, SENTINEL -0.736, POVID 0.114.
  - **Statistic.** D_b = Δm(POVID) − mean(Δm(HA-DPO), Δm(SENTINEL)), in classes per caption. It is positive when the chosen-fewer group shrinks its object count more.
  - **Verdict.** HELD iff D_b ≥ +0.3 and its 95% lower bound > 0. NOT_HELD otherwise.
  - **Kill (L6 §6).** If D_b < 0.1, prediction (b) is dropped and N9 "shows no Δk → Δm link". That is the second half of the conjunctive kill in Paper A §9 (L6 §6 D2). Its first half: RLAIF-V's chosen-fewer share among count-unmatched pairs lies in [0.45, 0.55] (`l6_d2_evaluation.kill_rule_rlaifv_in_045_055.in_kill_interval_all_obj_pairs` = true), so it has fired.
  - **Registered sensitivities** (reported, never a verdict):
    - D_b′, which adds RLAIF-V (training-data mean Δk -0.017) to the near-balanced group;
    - D_b computed with `n9_povid_fullmerge` in place of POVID.
- **(c) HALVA |Δm| ≤ 0.15. NOT TESTABLE in this registration**, because HALVA is excluded for lack of a licence statement (§1). It can only be revived by a committed addendum before any HALVA output exists; (c) would then be evaluated as written.

## 7. Kill rules and gates

- **K-F, fidelity (L6 §6; E1-K1 thresholds).** No method output is scored until the base passes this gate.
  - **Rule.** The base run's CHAIR_i and CHAIR_s are compared with LiM's published LLaVA-1.5-7B values on the same 500 images, read in code from `.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json` `fidelity_K1.lim_r1.published` (CHAIR_s 50.0, CHAIR_i 15.4, Recall 77.1). If |ΔCHAIR_i| > 1.0 or |ΔCHAIR_s| > 1.5, the protocol is fixed before any method look. The failed run is kept and disclosed.
  - **Descriptive.** The same scorer on LiM's released r1 captions gives CHAIR_s 50.5, CHAIR_i 15.26, Recall 77.5 (`e1_results.json` `systems["lim/r1-llava1.5-7b"]`), and the share of images whose N9 base caption equals LiM's released r1 caption exactly is reported.
- **K-b.** The kill on prediction (b), defined in §6.
- **K-headline (L6 §6).** If at least half of the methods (≥ 3 of 6) SURVIVE on P1, the headline becomes "training changes object choice". That still supports count-controlled reporting.
- **K-rank (PD-6 Q4(c)).** The count-matched ranking is compared with the raw ranking over the seven systems (six methods plus the base at 0).
  - **Significant reversal.** A pair (i, j) is significantly reversed if the sign of dP_raw,i − dP_raw,j differs from the sign of dP_C*,i − dP_C*,j, and the 95% bootstrap interval of dP_C*,i − dP_C*,j excludes 0.
  - **Consequence.** If no pair is significantly reversed, Paper A reports N9 as "consistent with the raw ranking" and rests no claim on it.
- **K-placebo (H6 P5).** If no control is admissible on K2, P1 has no primary control. N9 reports the three per-image controls as a specification curve and makes no "survives count control" claim, and Paper A's C1 wording becomes "count control changes the ranking".
- **K-protocol.** Any failure makes the affected run invalid. It is re-run before scoring, and the failure is disclosed. Every run must have:
  - the same prompt-ids sha256, the same id-list sha256, the same per-image image sha256s, the same decoding settings and the same batch size;
  - merged-module counts equal to §1;
  - a passed coverage check (the harness stops otherwise);
  - `hit_max_new_tokens` reported per run (descriptive).
- **K-licence.** A checkpoint whose licence statement changes to a non-open one before its run is dropped.

## 8. Analysis plan

1. **K2 first.** Decode `k2_seed1` and `k2_seed2`, apply the addendum's rules, and fix C*.
2. **Base, then fidelity.** Decode `n9_base` and apply K-F.
3. **Methods.** Decode all method runs plus `n9_povid_fullmerge`. Decoding is not a look. Nothing is scored until every run exists and K-protocol passes.
4. **Score once, with one script.** It must:
   - import `scripts/lvlm/e1_chair_count.py` unchanged and implement exactly §4 to §7;
   - be committed before the first K2 or N9 score is computed;
   - first reproduce E1's `pairs_15` values (`dP_MCP_prefix`, `dP_MCP_sent_tieavg`, `dP_MCP_rand_exact`, `dP_TRF_prefix`) on E1's released outputs, which is its correctness check;
   - read every number from JSON and compute every label by rule (`manuscript/verification/CHECKLIST.md` C1).
5. **Report everything,** whichever way it falls: Paper A Tab. 3 and §6.4 (raw, P1 under C*, the specification curve, P2, CAR, Δm, CHAIR_s and CHAIR_i), the predictions and every kill rule.

## 9. Deviations from L6 D1, fixed now (before any output)

- **Checkpoints.** Six of L6's eight checkpoints are run: HSA-DPO has no 7B or HF release, and HALVA has no licence statement. mDPO, named in prediction (b), has no checkpoint. So (b) uses the named groups as far as they are released, and (c) is not testable.
- **POVID ids.** The real ids are `YiyangAiLab/llava_POVID_stage_one_lora` and `YiyangAiLab/llava_POVID_stage_two_lora`. The README links `POVID_stage_one_merged` and `POVID_stage_two_LoRa` redirect to them; L6 wrote "POVID_stage_two_LoRa" with another owner, and that id returns 401.
- **OPA-DPO** is on Hugging Face (`zhyang2226/opadpo-lora_llava-v1.5-7b`), not only on Google Drive.
- **Count controls and resamples.**
  - The sentence tie-average and the frontier residual P2 are added (PD-2; Paper A §3.3(b)), and C* comes from the K2 rule (D17).
  - The bootstrap uses B = 5000, as PD-2 requires (E1 used 1,000 in the pilot and registered 2,000).
- **POVID's loading rule** and its sensitivity run are as in §1.
- **Cost.** About 0.25 GPU-h per run on an RTX 3090 at batch 8: eight N9 runs plus the two K2 runs.
