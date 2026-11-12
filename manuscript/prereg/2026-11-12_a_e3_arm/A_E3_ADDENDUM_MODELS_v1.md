# A-E3 addendum v1: second batch (parts 7c, 7d). Gemma-3-4B-it in a second environment, plus one further model (2026-11-12)

Written 2026-11-12, about 09:00–09:40Z (16:00–16:40 VN). Writer agent. The only host work was building the second environment and running the decoder's CPU self-test in it (`A_E3_ADDENDUM_BUILD_NOTE.md`). No model weights were fetched. No output, job log line or ledger value of 7a was opened by this writer. The 7a facts below are the coordinator's, from gate counts only. No LOG line, CC file or commit was made. "chưa kiểm" means not checked. Judgements are AI opinion.

**Binds:** run document v1.1 (`A_E3_ARM_RUN_DOC_v1_1.md`, `1df371cc…`), CC-349, CC-351 and CC-355. Everything in them stays in force unless a line below changes it. **Gate:** one-judge FULL read, REVERSIBLE, bar 85. Then the gatekeeper commits the files of §7, before any 7c decode.

## 0. Why this addendum

Facts at about 1.3 of 10 GPU-h, from the 7a job log (counts and gate values only, nothing opened):

| Order | Model | 7a result |
|---|---|---|
| 1 | Aya-Vision-8B | PASSED (D1 50/50) |
| 2 | Gemma-3-4B-it | MODEL FAIL at its first run, both attempts within seconds: `ValueError: Using or_mask_function or and_mask_function arguments require torch>=2.6` |
| 3 | Idefics3-8B | G4 share 0.000: not assessable |
| 4 | LLaVA-1.5-7B | G4 share 0.700: not assessable |
| 5 | SmolVLM2-2.2B | G4 1.000 on both prompts; decoding its 600-image runs |
| 6 | LLaVA-1.6-Mistral-7B | next |

- **Gemma's failure is an environment fault, not a model result.**
  - `/root/venv-lb` has torch 2.5.1+cu121 and transformers 4.57.6.
  - transformers 4.57.6 `masking_utils.py` l.808–816 and l.904–912 raise that error when a model passes an or/and mask function under `torch < 2.6`, which Gemma 3's mask code does.
  - Run document §3 checked only the transformers floor (≥ 4.50). It did not check the torch floor of the Gemma 3 mask code. The miss is ours.
- **The arm will likely end with two or three models** against the plan's target of four.
  - The candidate lost was the only one besides Aya with a documented multilingual card.
- **What this addendum adds:**
  - (a) Gemma-3-4B-it, unchanged, in a second environment that moves only torch and what torch pins;
  - (b) one new candidate, chosen by rules fixed before any model was named;
  - (c) two new parts, 7c (Vietnamese) and 7d (English), under the same cap, gates, prompts, decoding settings, sets and custody.
- **Approvals.** PI-1105k and PI-1107c approved one arm of up to 10 GPU-h on XM3600-600. The addendum stays inside that arm and that cap. AI view: no new PI decision is needed. Open point O1.

## 1. Disclosure the paper must carry (fixed now, before any 7c output exists)

> "Two models were added to this development arm after its first batch: Gemma-3-4B-it and Granite-Vision-3.3-2B. Gemma-3-4B-it was a registered candidate that could not run in the first software environment: its library code needs PyTorch 2.6 or later, and the environment had 2.5.1. It was run unchanged (same weights, prompts and decoding settings) in a second environment that differs only in the PyTorch, torchvision, Triton and CUDA-library versions. Granite-Vision-3.3-2B was chosen by written selection rules (language-model family, stock loading, chat template, memory, licence, a multilingual language-model card) fixed before any model was screened. Both were added after [two | three] registered candidates had failed the Vietnamese-share gate and one had failed on the library version. At that point only gate counts had been seen and no caption had been opened."

- Fill the bracket from the final 7a log: three if LLaVA-1.6-Mistral also fails G4.
- The sentence stays even if neither added model passes.
- Beside every row of an added model, print: "added after the first batch (A-E3 addendum); second software environment".

## 2. Models

### 2.1 Rules

**Brief rules B1–B6** were fixed by the coordinator's brief before any model was screened:
- B1: a language-model family not already passing, and not Qwen-based.
- B2: loads with stock `transformers` in one of the two environments, with `trust_remote_code=False`.
- B3: has a chat template usable by `apply_chat_template`.
- B4: fits in 24 GB at batch size 1 in bf16.
- B5: the licence is usable for research, and it is not gated beyond what is already accepted.
- B6: a documented multilingual language model, with the card line quoted and no Vietnamese ability claimed unless a card states it.

**Honest record:** the writer made the rules exact while screening. The table marks each **writer refinement (W)**. Every refinement only excludes a model. None was needed to admit Granite: it passes B1–B6 as written.

| Rule | Content | Origin |
|---|---|---|
| R1 family | Its language-model family (from `config.json` `text_config`, plan §4.2 l.181) is not Qwen and has not already passed (Command R / Cohere2 from Aya; SmolLM2 from SmolVLM2, if it passes). **W:** not Gemma either, since Gemma-3-4B already holds Gemma in this batch. | B1 + W |
| R2 loader | It loads with the pinned decoder unchanged: its `model_type` is in transformers 4.57.6 `MODEL_FOR_IMAGE_TEXT_TO_TEXT_MAPPING_NAMES`, with `trust_remote_code=False` and sdpa. **W:** no transformers fix that the model's own card asks for may be missing from 4.57.6. | B2 + W |
| R3 template | The **processor** has a chat template that accepts the decoder's message shape: a list of `{"type": "image"}` and `{"type": "text"}` items, rendered by `processor.apply_chat_template` (decoder l.208–211). | B3, made exact |
| R4 memory | It fits on one 24 GB GPU at batch 1 in bf16 (weights ≤ about 20 GB). **W:** weights are not quantised (no FP8 or 4-bit). | B4 + W |
| R5 licence | The licence allows research use. It is not gated beyond what is already accepted (Gemma's PI-1111h). | B5 |
| R6 multilingual | The VLM card, or the card of the language model it names, lists natural languages beyond English, with the line quoted. **W:** more than two languages, so a bilingual en+zh card does not count. | B6 + W |
| R7 not a reasoning model | **W:** the chat template does not open a thinking block before the answer, because the 60/160 caps would cut the caption off. | W |

**W ranking, if more than two pass:**
1. Vietnamese is named on a card.
2. More languages are listed.
3. One model per family: the newest version, then the largest that meets R4.

It was not needed: one model passed.

### 2.2 Gemma-3-4B-it: the same model, a new key

- **Key `gemma3_4b_lb26`.** The block is the v1 `gemma3_4b` block **byte for byte**: hub id `google/gemma-3-4b-it`, revision `093f9f388b31de276ce2de164bdc2081324b9767`, the 13 file pins (4 from the Hub's authenticated paths-info `lfs.oid`, CC-349 W6 / CC-351), bf16, sdpa, batch 1, `processor_kwargs {}`. Only the key is new. The inherited `role` text is stale (CC-351 N13) and is kept as a record.
- **Why a new key.** Each run id contains its key, and the decoder binds a partial file to its configuration. `run_key` hashes the registration's sha (decoder l.115–116, l.266). `open_partial` refuses a partial written under another configuration (l.125–126).
  - The 7a attempt probably left `ae3_gemma3_4b_xm600f50-short.preds.json.partial.jsonl` with the v1 key. The model was loaded before the error.
  - Under v2 the old run ids would therefore fail twice more.
  - New run ids (`ae3_gemma3_4b_lb26_…`) avoid this without touching `/root/a_e3/out`.
- **Snapshot.** The one fetched under OPS-1112r, reused read-only: `A_E3_SNAP_gemma3_4b_lb26=/root/a_e3/models/gemma3_4b`. G3 checks all 13 pins before any load. No new fetch.
- **Not tested:** whether Gemma 3 actually generates under torch 2.6. That is first seen in its first 50-image run, which is the smoke step (CC-349 Q8). A failure there is a MODEL FAIL (S3).

### 2.3 Every model screened (Hub API at 2026-11-12 08:50–09:00Z; unauthenticated; generic client)

| Model (revision) | LM (`text_config`) | R1 | R2 | R3 | R4 | R5 | R6 | R7 | Result |
|---|---|---|---|---|---|---|---|---|---|
| **ibm-granite/granite-vision-3.3-2b** (`bf66a824…`) | granite (granite-3.1-2b-instruct) | ok | `llava_next` in the 4.57.6 map; config written by 4.50.3; sdpa ok | `chat_template.json`, list content with image/text | 2.98 B, about 6.0 GB bf16 | apache-2.0, not gated | LM card: 12 languages (quoted in §2.4) | ok | **chosen** |
| SeaLLMs/SeaLMMM-7B-v0.1 (`58843a60…`) | mistral (SeaLLM-7B-v2) | Mistral; open only if order 6 fails G4 | `llava_next`, config from 4.39.0.dev0 | **fails**: `processor_config.json` has no template. The tokenizer template concatenates `message['content']` as a string, so a list of items breaks it | 7.69 B | custom "SeaLLMs Terms of Use" | card lists `vi` (the only screened card that does) | ok | out (R3). Using it would need new decoder code |
| LiquidAI/LFM2-VL-3B (`97a81f5c…`) | lfm2 (LFM2-2.6B) | ok | `lfm2_vl` is in 4.57.6 and loads by B2 as written. **Fails the W clause:** the card (l.107–110) asks for transformers built from source at `87be5595` (2025-10-22). That build has the fix #41755 ("Swap columns and rows of the grid layout in LFM2-VL … that were resulting in incorrect positional special tokens", merged 2025-10-22), which v4.57.6 lacks. Checked in code: `image_processing_lfm2_vl_fast.py` l.397 reads `images, num_rows, num_cols = self.crop_image_to_patches(` in v4.57.6 and `images, num_cols, num_rows = …` at `87be5595`. So under 4.57.6 a tiled non-square image gets wrongly placed tile tokens | `chat_template.jinja` ok | 3.0 B | LFM Open License v1.0: research use allowed (LICENSE l.31, l.57; the revenue threshold applies to commercial use); not gated | card metadata lists 10 languages, but the card body (l.71) says "Supported languages: English"; LM card LFM2-2.6B l.67: "English, Arabic, Chinese, French, German, Japanese, Korean, and Spanish" | the LM card (l.74) says LFM2-2.6B uses "dynamic hybrid reasoning (traces between `<think>` and `</think>` tokens) for complex or multilingual prompts" (W R7 partly) | **out by the W clause of R2 only. On B1–B6 as written it would be a second candidate.** Open point O11 |
| LiquidAI/LFM2-VL-1.6B (`2c2e7f9b…`) | lfm2 | ok | same l.397 issue | ok | 1.6 B | same licence | card `en` only; LM LFM2-1.2B (chưa kiểm) | – | out (R2 W; one per family) |
| mistralai/Ministral-3-8B / 3B-Instruct-2512 | ministral3 | – | **fails**: `ministral3` is not in 4.57.6 (config from 5.0.0.dev0) | – | **FP8** weights | apache-2.0 | 11 languages | – | out (R2, R4) |
| google/gemma-3n-E4B-it | gemma3n | **Gemma**, already held by `gemma3_4b_lb26` | ok | – | 7.85 B | gated (Gemma) | – | – | out (R1) |
| facebook/Perception-LM-3B / 8B | Llama 3.2 / 3.1 (chưa kiểm, from memory) | ok | ok | – | ok | **gated manual, not accepted** | `en` | – | out (R5) |
| deepseek-community/deepseek-vl-7b-chat, Janus-Pro-7B | DeepSeek LLM | ok | ok | – | ok | other / MIT | no language list on the card | – | out (R6) |
| BAAI/Emu3-Chat-hf | Emu3 | ok | ok | – | 8.76 B | apache-2.0 | `en` | – | out (R6) |
| zai-org/GLM-4.1V-9B-Thinking | glm4 | ok | `glm4v` ok | ok | 10.3 B, about 20.6 GB, tight | MIT | `en`, `zh` | **thinking model** | out (R6, R7) |
| Pixtral-12B, Mistral-Small-3.1-24B, Aya-Vision-32B, Llama-4, Gemma-3-12B | – | – | – | – | **> 24 GB** (chưa kiểm per model except Gemma-3-12B, run doc §2.2) | – | – | – | out (R4) |
| Llama-3.2-11B-Vision | Llama 3.1 | – | – | – | – | **gate not accepted** (PI-1111h) | – | – | out (R5) |
| InternVL3/3.5-hf, Ovis2, LLaVA-OneVision, Qwen-VL | Qwen (InternVL3: CC-184; the others chưa kiểm, from memory) | **Qwen** | – | – | – | – | – | – | out (R1) |
| Phi-4-multimodal, Phi-3.5-vision, MiniCPM-V, Molmo, Kimi-VL, InternVL2.5, DeepSeek-VL2 | – | – | **fails**: none of these `model_type`s is in the 4.57.6 map (checked), and they need remote code (chưa kiểm, from memory) | – | – | – | – | – | out (R2) |
| idefics2-8b, bakLlava, llava-phi-3, llama3-llava-next, fuyu, chameleon | Mistral / Llama / Phi / Persimmon | – | ok | – | ok | chameleon gated | English-only cards (chưa kiểm, from memory) | – | out (R6 or R5) |

**Result: in this screen, only one new model passes R1–R7:** Granite-Vision-3.3-2B. **No second candidate was found** under these rules and the pinned transformers 4.57.6. The screen did not enumerate community fine-tunes on the `llava` / `llava_next` architectures. LFM2-VL-3B is the nearest miss. It is excluded only by a writer refinement, so the judge decides it (O11). The run document's target of four is reached only if enough of {Aya, SmolVLM2, LLaVA-1.6-Mistral, Gemma, Granite} pass.

### 2.4 The new model

| Field | Value |
|---|---|
| Key | `granite_vision33_2b` |
| Hub id @ revision | `ibm-granite/granite-vision-3.3-2b` @ `bf66a8244401a8e26d2ff429aa82df8550a289e5` (= main on 2026-11-12; last modified 2026-04-02) |
| Licence, gate | apache-2.0; not gated (revision API `gated: false`) |
| Language model | Granite 3.1 2B Instruct (`text_config.model_type` `granite`, `_name_or_path` `ibm-granite/granite-3.1-2b-instruct`) |
| Vision encoder | `siglip_vision_model`, hidden 1152, 27 layers, patch 14, 384 px (the SigLIP so400m shape); multi-layer features [-24, -20, -12, -1]; LLaVA-NeXT any-resolution tiling |
| Parameters | 2,975,396,928 (Hub `safetensors.total`, all BF16) |
| Memory | about 6.0 GB of bf16 weights. With the processor's default any-resolution tiling, the activations at batch 1 are far below 24 GB (AI estimate) |
| Files pinned | 14: every file except `README.md`, `.gitattributes` and `example.png`. Two safetensors by `lfs.oid` (sha256), 12 by git blob sha1. All taken from the tree API at the revision; nothing was hashed from a fetched file. Values are in `A_E3_REG_v2.json` |
| Card lines (quoted) | VLM card l.36: "Currently the model supports English instructions and images (png, jpeg) as input format." LM card (`ibm-granite/granite-3.1-2b-instruct` @ `bbc2aed5`, l.26–27): "Supported Languages: English, German, Spanish, French, Japanese, Portuguese, Arabic, Czech, Italian, Korean, Dutch, and Chinese." |
| Vietnamese | **not documented** on either card |
| Harness notes (disclosed) | Its chat template inserts an English default system line when none is given ("A chat between a curious user and an artificial intelligence assistant…"). The harness passes none, as for every model. The card targets document understanding (tables, charts) |

**Expectation (AI opinion):** Granite will probably fail G4 on the Vietnamese prompts. The VLM card says English instructions, and the template adds an English system line. It costs about 0.1 GPU-h to find out: two 50-image runs and two loads. It is included because it meets the rules, and leaving it out because it might fail would be a choice made on expected results. Open point O3.

### 2.5 Order in 7c

1. `gemma3_4b_lb26` (the registered order-2 model, restored);
2. `granite_vision33_2b`.

7c stops at four passing models in total. In the job, NEED for 7c is 4 − |passed_7a.txt|, the same "first four that pass" rule as 7a. So **five** passing models are unreachable: if 7a passes three, 7c stops at the first pass. Open point O4.

## 3. Second environment `/root/venv-lb26`

**Recipe** (built on hc2 2026-11-12, 09:05–09:18Z (second try; the first try, 08:58–09:03Z, failed before installing anything), under `nice -n 19 ionice -c3`; commands in the build note):

```
/usr/bin/python3.10 -m venv /root/venv-lb26                        # same interpreter as venv-lb (3.10.22); pip 23.0.1 as in venv-lb
/root/venv-lb/bin/python -m pip freeze > lb.freeze                  # venv-lb freeze, sha 685ffe2a… (= H_LB)
grep -v -E '^(torch|torchvision|triton|nvidia-[a-z0-9-]+)==' lb.freeze > rest.txt     # 28 lines
/root/venv-lb26/bin/python -m pip install --no-cache-dir --no-deps -r rest.txt   # every other package == venv-lb, no resolution
/root/venv-lb26/bin/python -m pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cu124 torch==2.6.0+cu124 torchvision==0.21.0+cu124
/root/venv-lb26/bin/python -m pip check
```

The `--no-deps` pins come first, so that accelerate's `torch>=2.0` cannot pull a PyPI torch. The torch step then adds only what torch itself pins (triton, the nvidia-* wheels) from the cu124 index. A first try in the other order failed before installing anything: the cu124 index lacked a build dependency (`flit_core`) for an sdist of typing_extensions. The venv was deleted and rebuilt (build note).

- **Why cu124.** The PyTorch index has no cu121 build of torch 2.6.0 for cp310. cu124 is the nearest; it has `torch-2.6.0+cu124` and `torchvision-0.21.0+cu124`, and the host driver 580.126.09 supports it.
- **torch 2.6.0** is the lowest version that clears the `>= 2.6` check.
- **What moved, against venv-lb (full freezes in the build note):**

| Package | venv-lb | venv-lb26 |
|---|---|---|
| torch | 2.5.1+cu121 | 2.6.0+cu124 |
| torchvision | 0.20.1+cu121 | 0.21.0+cu124 |
| triton | 3.1.0 | 3.2.0 |
| nvidia-cublas-cu12 | 12.1.3.1 | 12.4.5.8 |
| nvidia-cuda-cupti-cu12, -nvrtc-cu12, -runtime-cu12, nvidia-nvtx-cu12 | 12.1.105 | 12.4.127 |
| nvidia-cufft-cu12 | 11.0.2.54 | 11.2.1.3 |
| nvidia-curand-cu12 | 10.3.2.106 | 10.3.5.147 |
| nvidia-cusolver-cu12 | 11.4.5.107 | 11.6.1.9 |
| nvidia-cusparse-cu12 | 12.1.0.106 | 12.3.1.170 |
| nvidia-nvjitlink-cu12 | 12.9.86 | 12.4.127 |
| nvidia-cusparselt-cu12 | – | 0.6.2 (new; required by torch 2.6.0) |

Everything is pinned by torch 2.6.0+cu124's own requirements. The freeze has 43 lines in venv-lb and 44 in venv-lb26. nvidia-cudnn-cu12 9.1.0.70 and nvidia-nccl-cu12 2.21.5 are unchanged.

- **Unchanged:** every other line, in particular transformers 4.57.6, accelerate 1.15.0, tokenizers 0.22.2, huggingface_hub 0.36.2, safetensors 0.8.0, pillow 12.3.0, numpy 2.2.6, num2words 0.5.14, Jinja2 3.1.6.
- **Registered values:**
  - `venvs.lb26.packages` = `{"torch": "2.6.0+cu124", "torchvision": "0.21.0+cu124", "transformers": "4.57.6", "accelerate": "1.15.0"}` (the four the decoder checks, l.254, read from the built environment);
  - `venvs.lb26.freeze_sha256` = `396626b4c55db0deb5bd6b7738a4b0740ca0ae5d3ba5b77b5950de375580ed51`, in the job's own form `$PY -m pip freeze | sha256sum`;
  - `venvs.lb.freeze_sha256` = `685ffe2a0100ce2489cccd77313d366fb1dce4455871a9d82f65aa139fa85784` (H_LB, CC-351 LC1).
- **Checks run in it** (CPU only, `CUDA_VISIBLE_DEVICES=""`, a throw-away copy of the decoder code from HEAD, sha-equal to SHA256SUMS_E3):
  - `transformers.masking_utils._is_torch_greater_or_equal_than_2_6` = `True` (`torch.version.cuda` 12.4);
  - the 4.57.6 image-text-to-text map contains `gemma3` and `llava_next`;
  - `decode_hf_vlm.py --selftest` (tiny random LLaVA, no `--prereg`): rc 0, 15 PASS lines and `selftest ok` (log `selftest_lb26.log` sha256 `165a7200f82ab953509c10253a807a578ebc803bbad016a3658d8682ca9ffd08`; the only other lines are two library warnings: slow image processor, `torch_dtype` deprecated).

**How the environment of each model is fixed and enforced.**
1. `A_E3_REG_v2.json` holds `venvs` {lb, lb26} with packages and freeze sha, and `model_env` {key → lb | lb26}. The six v1 models map to `lb`; `gemma3_4b_lb26` and `granite_vision33_2b` map to `lb26`.
2. Top-level `venv` in v2 = the lb26 block. The decoder (l.254) then refuses any v2 run whose four package versions are not lb26's. 7a/7b keep running under v1, which refuses anything but lb's versions. So **a part, its registration and its environment are tied**: 7a/7b = v1 = lb, and 7c/7d = v2 = lb26. A real per-model switch inside one part is not built, because no 7c/7d model needs lb.
3. The job (7c/7d) checks, before any decode, that **every model of the part's order** has a registered freeze equal to the job's `VSPS_VENV_FREEZE_SHA256`. Otherwise it is a JOB STOP (S1).
4. **Pull rule, extended.** CC-351's rule held an output whose freeze was not H_LB. It becomes: every `.preds.json` has `venv_freeze_sha256` = `venvs[model_env[model]].freeze_sha256` of A_E3_REG_v2.json, and the same for its `packages`. Any other value means that output is HELD and goes to a judge line. The 7a/7b outputs are checked against `lb` (= H_LB, as before), and 7c/7d against `lb26`.

## 4. What does not change

- **Prompts, decoding and sets:**
  - prompts: the four hashes of run doc §3;
  - caps: 60/160;
  - greedy, batch 1, default image processing;
  - sets: `xm600`, `xm600f50`, manifests unchanged;
  - decoder: `e2de1881…`, unchanged.
- **Gates G0–G6 and stop rules S1–S8:** the same code paths in the job (`dec`, `lang_ok`, `d1_ok`, the G6 projection, the S4 counter per part).
  - 7c applies the 7a gates (G4 Vietnamese share ≥ 0.95 on both prompts).
  - 7d applies the 7b gates (English share with the W3 definition).
  - 7d runs only the models in `passed_7c.txt`.
- **Custody (§7):** unchanged. Added: the job also stops if `topup1/` exists in its tree (§5.3).
- **Job changes:** exactly those in `A_E3_JOB_V2.diff`:
  - parts 7c/7d (registration and Python per part);
  - the 7c order and NEED;
  - the per-model freeze check;
  - `SHA256SUMS_E3_V2` in place of `SHA256SUMS_E3` (the old file pins the old job sha);
  - the topup1 custody line;
  - "reg" in the START line;
  - comments.
- **Separate, refusable:** the two CC-351 carried items N2' and N10 (build note §4).

## 5. Parts, order, cap, host layout, top-up

### 5.1 Parts

| Part | Registration / env | Models | Runs per model | Gate |
|---|---|---|---|---|
| 7c | v2 / lb26 | `gemma3_4b_lb26`, then `granite_vision33_2b`, stopping at 4 − \|passed_7a\| passes | `xm600f50-{short,detailed}` (G4), then `xm600-{short,detailed}` (G5 D1) | as 7a |
| 7d | v2 / lb26 | `passed_7c.txt` | the same with `short_en`, `detailed_en` | as 7b |

Outputs go to the same `/root/a_e3/out`. The files are `passed_7c.txt`, `passed_7d.txt`, `SHA256SUMS_7c`, `SHA256SUMS_7d` and `selftest_7c.log`. The ledger, `checks.log`, `job.log` and the RUNNING lock are shared.

### 5.2 Order (recommended)

1. 7a runs to `JOB DONE 7a` (registered job, unchanged).
2. Pull 7a and verify it per §8. The 7a copy of record stays 444.
3. **7c** starts from the second clone (§5.3). The job itself refuses 7c unless `job.log` holds a `JOB DONE 7a` line. The operator starts it only after the 7a pull is verified.
4. Pull 7c into a **separate** laptop dir (`…/ATTR_H1_7c/root/a_e3/out/`), so that the 444 7a copy is never rewritten. Run `sha256sum -c SHA256SUMS_7c`, sidecars, digest, 444, and an OPS line with `passed_7c.txt`.
5. **7b**, from the **original clone at 26574ef with the registered job** (literally unchanged, as CC-351 approved).
6. **7d**, from the second clone.
7. Pull 7b + 7d (separate dir), wipe the tmpfs, delete the host when no approved job remains.

Why 7c before 7b:
- The top-up build needs **all** Vietnamese runs (7a + 7c), and there is one top-up session only (CC-349 Q11).
- 7c before 7b hands the top-up over about 2–4 h earlier (the length of 7b, AI estimate).
- The GPU stays busy in either order.
- Cost: 7c is placed ahead of 7b in the cap's cut order (S5 said "7a first, 7b's last models go first"). A cap shortfall therefore cuts English runs first, never Vietnamese ones. Open point O2.

**If the addendum commit is not in place at `JOB DONE 7a`:** run 7b first (no change needed), then 7c and 7d. The GPU never waits for this addendum.

### 5.3 Host layout for 7c/7d

- **Second sparse clone** at the addendum commit: `/root/a_e3/vsps2`. Same sparse set as run doc §7, plus the exclusion `'!/manuscript/prereg/2026-11-12_a_e3_arm/topup1/'`:

  ```
  git clone --filter=blob:none --sparse <repo> /root/a_e3/vsps2 && cd /root/a_e3/vsps2 && git checkout <addendum commit>
  git sparse-checkout set --no-cone /scripts/a_e3/ /scripts/lb/ /scripts/g2b/decode_qwen3vl.py /scripts/evaluate.py /rescap/ /manuscript/prereg/2026-11-12_a_e3_arm/ '!/manuscript/prereg/2026-11-12_a_e3_arm/topup1/'
  ```

  - The running 7a job's tree `/root/a_e3/vsps` is never updated, so bash never reads a script that changed under it.
  - The public top-up copy (`topup1/assignment.json`, run doc §9.1 step 6), if committed later, never reaches the host. The job line `[ ! -e "$PRE/topup1" ]` enforces this.
- **Granite fetch:** after the commit, while 7a still decodes. Network and disk only, `nice -n 19 ionice -c3`, `HF_HOME=/root/a_e3/hf`, no token (not gated), `df -BG /root` ≥ 40 G after:
  `HF_HUB_OFFLINE=0 /root/venv-lb26/bin/python -I -B scripts/lb/decode_hf_vlm.py --prereg manuscript/prereg/2026-11-12_a_e3_arm/A_E3_REG_v2.json --fetch granite_vision33_2b --snapshot /root/a_e3/models/granite_vision33_2b` (from vsps2). About 6 GB.
- **Launch lines (tmux, from vsps2):**
  - `A_E3_PART=7c A_E3_SNAP_gemma3_4b_lb26=/root/a_e3/models/gemma3_4b bash scripts/a_e3/a_e3_job.sh`
  - later `A_E3_PART=7d A_E3_SNAP_gemma3_4b_lb26=/root/a_e3/models/gemma3_4b bash scripts/a_e3/a_e3_job.sh`
- **Launch conditions (operator):**
  - L1: the commit exists, `git rev-parse HEAD` in vsps2 = it, there is no `data/` and no `topup1/`, and `bash -n` is OK.
  - L2: `/root/venv-lb26/bin/python -m pip freeze | sha256sum` = `396626b4c55db0deb5bd6b7738a4b0740ca0ae5d3ba5b77b5950de375580ed51`.
  - L3: `--check-snapshot gemma3_4b_lb26 --snapshot /root/a_e3/models/gemma3_4b` prints "13 pinned files ok", and the same for granite ("14").
  - L4: the 7a pull is verified (OPS line written).
  - L5: no compute process on the GPU.
  - L6 (the CC-351 LC3 analogue): within the first minutes, `pins.log` shows gemma ok. If `job.log` shows `SKIP gemma3_4b_lb26`, the launch variable was omitted. Kill the job at once, log a DEVIATION and relaunch with the variable. Finished outputs are kept; the operator adds the killed attempt's seconds by hand (N11). Otherwise Gemma would be lost silently a second time.

### 5.4 Cap: one ledger, one 36,000 s

- `spent()` sums **every** row of `/root/a_e3/out/ledger.tsv`: all attempts of all parts, loads included. 7c and 7d therefore see what 7a (and 7b, if it ran first) spent. Nothing resets.
- The G6 pre-check (spent + 600 × the model's 50-image rate ≤ 36,000) and the per-attempt cut to `36,000 − spent` apply unchanged.

| Item | GPU-h | Basis |
|---|---|---|
| Spent at brief time | about 1.3 | coordinator, from the job log (not read by this writer) |
| Rest of 7a: SmolVLM2 600-image runs; LLaVA-1.6 50-image runs (+ 600-image runs if it passes G4) | 0.5–1.0 (+0.9–1.8) | run doc §10 rates; SmolVLM2 is 2.2 B |
| 7c: Gemma (passes) + Granite 50-image runs only (fails G4) | 0.7–1.4 | run doc §10 Gemma row; 0.1 for Granite |
| 7c, if Granite also passes | +0.7–1.3 | anyres tiling; projection |
| 7b: Aya + SmolVLM2 (+ LLaVA-1.6) | 1.3–2.8 (+0.8–1.6) | run doc §10 |
| 7d: Gemma (+ Granite) | 0.5–1.1 (+0.5–1.0) | – |
| **Total, likely case** | **about 4.3–7.6** | under 10 |
| **Total, every model passing** (only if O4 lifts the stop at four; otherwise unreachable) | **about 7–13** | the cap may cut 7d, then 7b's last models |

All rows except the first are projections, not measurements. The exact figure is `gpu_s` in each `JOB DONE` line.

- **PI line (CC-349 ruling 4, extended; open point O5).** Asked only if a CAP STOP actually happens in 7b or 7d, or at `JOB DONE 7c` if spent + the projections of the English parts still to run > 36,000 s. Question: may the cap rise from 10 to 14 GPU-h, for the English parts only? Recommended: yes (money is not a constraint, PI 11-10). Default if the PI is silent: the English runs that fit under 10 run, and the rest are NOT RUN.

### 5.5 Top-up hand-over (needs changes to CC-355; open point O6)

- The top-up build waits for **both** Vietnamese pulls, 7a and 7c. The session itself already waits for the part-1-finished line (CC-355 ruling 4), so the wait for 7c usually costs nothing.
- **If 7c passes no model,** the build uses 7a alone, as now.
- **Text to change before the build** (each "open for the judge"):
  - **CC-355 LC2:** add "`JOB DONE 7c`, then §8 steps 1–3 on the 7c pull copy (`SHA256SUMS_7c` all OK, sidecars, digest, 444, OPS line with `passed_7c.txt`)".
  - **LC3:** the `--extra` list adds `ae3_<k>_xm600-{short,detailed}.preds.json` for every k in `passed_7c.txt`, from the 7c copy.
  - **LC4:** `counts.new_systems` = {…: k in passed_7a.txt ∪ passed_7c.txt}. Every `--extra` sha equals its line in `SHA256SUMS_7a` **or** `SHA256SUMS_7c`.
  - **A-CERT addendum E3 v1** (`64fad518…`) l.20: "Only models listed in the pulled `passed_7a.txt`" becomes "… `passed_7a.txt` or `passed_7c.txt`". This must be committed before any top-up label value is opened (it binds then).
  - **Annex B scoring note v1** (`0d30938b…`) l.10 and l.31: `passed_7a.txt` gains `passed_7c.txt`. The note must be committed before the 7c pull content is opened.
  - **Run doc §9.1 step 3** wording follows.
- **Not changed:** `build_topup.py` (954dd7b9): it takes any `--extra` list.

## 6. Paper wording (run doc §2.3 style; families from `config.json` at the pin; no "non-Qwen", no lineage sentence)

Read at the pin before printing:
- Aya: Command R7B, `cohere2`; SigLIP2.
- SmolVLM2: SmolLM2-1.7B; its `text_config.model_type` reads `llama`, so print the language model's name, not "Llama"; SigLIP (chưa kiểm).
- LLaVA-1.6-Mistral: Mistral-7B-Instruct-v0.2; CLIP ViT-L/14-336.
- Gemma-3-4B-it: Gemma 3; SigLIP.
- Granite-Vision-3.3-2B: Granite 3.1 2B Instruct; SigLIP.

Each sentence below is followed by the §1 disclosure sentence when an added model is among those counted.

- **Two pass** (e.g. Aya-Vision-8B, Gemma-3-4B-it): "Two further models, Aya-Vision-8B and Gemma-3-4B-it (language models Command R7B and Gemma 3), were decoded under the same settings. The other candidates did not write Vietnamese often enough to be scored (G4 counts in Table S-x)."
- **Three pass** (e.g. Aya-Vision-8B, SmolVLM2-2.2B, Gemma-3-4B-it): "Three further models, Aya-Vision-8B, SmolVLM2-2.2B and Gemma-3-4B-it, use three different language models (Command R7B, SmolLM2-1.7B, Gemma 3) and two vision-encoder lines (SigLIP2, SigLIP). …"
- **Four pass** (e.g. Aya-Vision-8B, SmolVLM2-2.2B, Gemma-3-4B-it, Granite-Vision-3.3-2B, or with LLaVA-1.6-Mistral-7B in place of Granite): "Four further models, Aya-Vision-8B, SmolVLM2-2.2B, Gemma-3-4B-it and Granite-Vision-3.3-2B, use four different language models (Command R7B, SmolLM2-1.7B, Gemma 3, Granite 3.1) and two vision-encoder lines (SigLIP2, SigLIP). Two of them (Gemma-3-4B-it, Granite-Vision-3.3-2B) were added after the first batch (see the disclosure)." With LLaVA-1.6-Mistral: replace "Granite 3.1" by "Mistral 7B" and "two vision-encoder lines (SigLIP2, SigLIP)" by "three vision-encoder lines (SigLIP2, SigLIP, CLIP)".
- **Five pass** (reachable only if the judge lifts the stop at four, O4): "Five further models, Aya-Vision-8B, SmolVLM2-2.2B, LLaVA-1.6-Mistral-7B, Gemma-3-4B-it and Granite-Vision-3.3-2B, use five different language models (Command R7B, SmolLM2-1.7B, Mistral 7B, Gemma 3, Granite 3.1) and three vision-encoder lines (SigLIP2, SigLIP, CLIP). …"
- **One or none pass:** S6 applies (no family comparison, no Annex B slope row). The disclosure sentence still prints.
- **Never:** "Vietnamese-capable" for Granite, SmolVLM2 or LLaVA-1.6. Their cards do not say so. G4 measures only whether the captions contain Vietnamese letters or tone marks.

## 7. Files (the gatekeeper commits these; sums in `SHA256SUMS_E3_V2`)

| File | Status |
|---|---|
| `manuscript/prereg/2026-11-12_a_e3_arm/A_E3_ADDENDUM_MODELS_v1.md` | this file |
| `manuscript/prereg/2026-11-12_a_e3_arm/A_E3_REG_v2.json` | v1 + `venvs`, `model_env`, 2 models, 16 runs; `venv` → lb26 (its `statement` lists every difference and self-checks them) |
| `scripts/a_e3/a_e3_job.sh` | new version (sha in SHA256SUMS_E3_V2); the registered v1.1 job `b11a9f6b…` stays in git history and stays live in the original clone |
| `scripts/a_e3/A_E3_JOB_V2.diff` | `diff -u` of v1.1 → new |
| `manuscript/prereg/2026-11-12_a_e3_arm/SHA256SUMS_E3_V2` | the SHA256SUMS_E3 lines with the job line updated, plus REG_v2 and this file |
| `manuscript/prereg/2026-11-12_a_e3_arm/A_E3_ADDENDUM_BUILD_NOTE.md` | build record (host commands, freezes, selftest) |

## 8. Open points for the judge (each with the recommended answer)

| # | Question | Recommended |
|---|---|---|
| O1 | Does adding two models inside the same arm and cap need a new PI line? | No. The same arm, the same 10 GPU-h, the same set. Disclosed (§1). |
| O2 | Run 7c before 7b, which puts 7c ahead of 7b in the cap's cut order? | Yes. The Vietnamese runs feed the top-up and the paper's claim, and the top-up hand-over comes earlier. If the commit is late, 7b runs first. |
| O3 | Include Granite-Vision-3.3-2B although its card says English instructions? | Yes. It meets R1–R7, costs about 0.1 GPU-h to test, and leaving it out on expected results is a selection by outcome. |
| O4 | Keep "stop at four in total" for 7c (5 unreachable)? | Yes. It is the run document's rule. Lifting it costs up to 1.3 GPU-h more for 7c and 7d. |
| O5 | PI cap line extended to `JOB DONE 7c` and to 7d CAP STOPs? | Yes, the same question (10 → 14, English parts only). |
| O6 | The CC-355 LC2–LC4, A-CERT E3 l.20 and Annex B note l.10/l.31 changes of §5.5? | Accept. Commit them as one short text package with a one-judge diff read, before the top-up build. |
| O7 | Second clone `/root/a_e3/vsps2` with the topup1 exclusion, and 7b from the original clone with the registered job? | Accept. No running script is ever replaced, and 7b stays byte-identical. |
| O8 | Separate laptop pull dirs per later part (7c, then 7b + 7d), so the 444 7a copy of record is never rewritten? | Accept. Run doc §8 step 1 names only one path. |
| O9 | The CC-351 N2' and N10 fixes in the same job version (build note §4)? | Accept, or refuse by reverting the four marked lines. |
| O10 | Gemma under torch 2.6 is untested until its first 50-image run (no weights may be loaded before the commit). | Accept. That run is the smoke step, as for every model (CC-349 Q8). |
| O11 | LFM2-VL-3B (LFM2 family; LM card lists 8 languages; research licence; not gated) passes the brief's rules B1–B6 as written. It is excluded only by the writer's R2 refinement: under 4.57.6 its tile grid has the row/column swap fixed by #41755 (l.397), which its card's required build contains. Add it as a third model under that known defect, or keep it out? | Keep it out. Decoding it under a known preprocessing bug would make its captions a test of the bug, not of the model. Fixing it would mean a third environment with transformers moved, which the brief rules out. Disclose it in the supplement as screened and excluded, with the reason. If the judge admits it, it is registered at `97a81f5c18b73352134099952a4856e2553d42d7` with tree-API pins in a v2.1 registration, as order 3 of 7c, and the defect is disclosed beside its rows. |
| O12 | The writer refinements W (R1 Gemma, R2 card-fix clause, R4 no quantisation, R6 more than two languages, R7, the ranking) were made exact during the screen. Accept them as part of this registration? | Accept. Each only excludes, none admitted Granite, and each is stated with its excluded models in §2.3. |
