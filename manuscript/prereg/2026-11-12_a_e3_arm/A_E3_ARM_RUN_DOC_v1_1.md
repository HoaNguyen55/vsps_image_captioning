# A-E3 run document v1.1: Paper A other-family development arm on XM3600-600 (2026-11-12)

Written 2026-11-11T23:20Z (06:20 VN, 11-12). Writer agent. Nothing was run, rented, fetched or committed, and no LOG line was written. No caption text, label value or `~/vsps_labels/` file was opened. Judgements are AI opinion. "chưa kiểm" = not checked.

**v1.1** written 2026-11-12T02:45Z (09:45 VN) from v1 (sha256 `f0a375fb…`) by `build/make_run_doc_v1_1.py`, for CC-349 (conditional GO 86). No decode before the round-2 diff read (CC-349r2) reads "W1-W7 CLOSED, no new BLOCKING" and the gatekeeper commit.

**Changes from v1** (each by its CC-349 item; nothing else changed):
- **CC-349 decision**: title names v1.1.
- **W7**: §0: the host is hc2, not a second host.
- **W5**: §1 draft disclosure: four of the twelve stored sets (Qwen3-VL T05/T08) are sampled, not greedy.
- **W7**: §2.1 Aya cell: literal path of C's copy.
- **Q3**: §2.1 Gemma pins: from the Hub API LFS sha256 only (ruling 2).
- **Q14**: §2.3: no lineage sentence; name the language models only.
- **W1-W4**: §4: the job script was revised; its sha is the one in SHA256SUMS_E3.
- **W4**: §6.2 G1: the custody gate.
- **W3**: §6.2 G4: an English caption needs at least one ASCII letter.
- **N1**: §6.2 G4: the 50-image outputs decoded so far are kept.
- **W1**: §6.2 G6: the cap is hard on every attempt.
- **W1**: S3: timeouts are cut to the cap remaining.
- **W2**: S4: coded with a counter.
- **W1, Q1**: S5: the cap is hard; cut order; when the PI line is asked (ruling 4).
- **W7**: §7: host choice set to hc2 (ruling 3).
- **W7**: §7: layout is hc2's.
- **W7**: §7: Aya reuse path is literal.
- **W7**: §7: on hc2 orders 2-5 are fetched (Aya reused, ruling 3 S-2); SmolVLM2 only if df allows (ruling 3(c)).
- **W4**: §7 custody: true for hc2.
- **W7**: §8 step 5: no second host to delete.
- **W7**: §9.1: pull path on hc2.
- **W7**: §9.3 timing: the hc2 line.
- **W7**: §10: earliest finish on hc2.
- **W7, Q5**: §12 Q5: hc2.
- **N6, Q8**: §12 Q8: no separate dry run.
- **Q11**: §12 Q11: one session after all of 7a; split not licensed.
- **Q14**: §12 Q14: no lineage sentence.
- **Q1-Q14**: §12: CC-349's answers recorded under the table.


## 0. Status and label

- **Label of every output and row:** DEVELOPMENT / A-E3, descriptive, no verdict. The images are spent: Paper A's registered look on XM3600-600 is used, and the set is dev-only (PORTFOLIO_3Y §2.3, l.191). Every printed row carries the words "new decodes on previously analysed images".
- **Approvals:** PI-1105k (LOG l.1608: one RTX 3090 rental day, cap 10 GPU-h, dev arm on XM3600-600) and PI-1107c (LOG l.1757). ERRATUM-1111-A-E3 (LOG l.2132): no new PI decision is needed. The PI agreed to a second RTX 3090 host (coordinator brief, 11-12); under CC-349 ruling 3 the arm runs on hc2 instead (§7).
- **Plan:** `manuscript/directions/A_UPGRADE_PLAN_2026-11-04.md` step 7 (l.232), §4.2 (l.176–182), §4.3 (l.203–211).
  - 7a = four models × two Vietnamese prompts × 600 images = 4,800 captions.
  - 7b = the same four models × two English prompts × 600 = 4,800 captions.
- **Gate for this file:** one-judge FULL read, REVERSIBLE, bar 85 (plan §5 step 7). Then the gatekeeper commits this file, the registration JSON, the two manifests, `SHA256SUMS_E3` and the job script before any decode.
- **What it registers:** decoding only. No hypothesis. Scoring rows come in Annex A (top-up labels) and Annex B (existing golds). Each annex binds only when committed before anyone opens an output it governs.

## 1. How Paper A's stored XM3600-600 outputs were decoded

| Stored family | Decoder | Batch | Greedy | New-token cap | Image input |
|---|---|---|---|---|---|
| Qwen2.5-VL-7B: six systems (`xm3600_{zeroshot,p1_s43,fuse2_s42}-{short,detailed}`) | `scripts/evaluate.py` at 34138e7 (`generate`): one `processor(text=[text], images=[image])` and one `model.generate` per image (`git show 34138e7:scripts/evaluate.py`, l.234–257). Job `62_58_z_xm3600_eval` on O-2293440 | **1** | `do_sample=False` | `--max-new-tokens`, default 160; the short runs' flag value is not in any stored record, and the job file is not in the repo (chưa kiểm). The longest stored short caption has 38 words | min 256 × 28², max 512 × 28² pixels |
| Qwen3-VL-8B, second backbone (`g2b_q3_xm600-*`) | `scripts/g2b/decode_qwen3vl.py` 8a855ef4 (`decode_items`, l.156–175: one `generate(i, f)` per image) | **1** | T0 greedy; T05/T08 sampled | short 60, detailed 160 (G2-B registration c506bc77 `decode.max_new_tokens`; file `max_new_tokens` 60) | min 262,144, max 1,048,576 pixels |

**Finding: both stored families were decoded one image at a time.** This arm also decodes at batch size 1, so there is **no batch-size difference** on XM3600-600.

The real differences are harness differences, and they must be disclosed:
- generic Auto-class loading through each model's own chat template, with the image inside the message (`decode_hf_vlm.py` l.181–220), instead of model-specific Qwen code;
- each model's default image processing (`processor_kwargs {}`, as in A-N2 and A-T3);
- caps of 60/160 new tokens, which equal the second backbone's and may differ from the first family's short cap.

Draft disclosure (supplement): "All captions on the 600 XM3600 images were decoded one image at a time; the four added models and the greedy (T0) stored systems used greedy decoding, the T05/T08 Qwen3-VL sets temperature sampling. The added models were run through one generic harness with their own chat templates and default image processing, with caps of 60 (short) and 160 (detailed) new tokens."

Not this arm, but relevant to the paper: Paper A's other decodes were **batched**:
- the A-N2 eight-LVLM ladder used registered batch sizes 2–8 (`2026-10-19_a_n2_lvlm_gold_ladder.json`, `models.*.batch_size`);
- A-T3 on COCO used the registered batch sizes of its registry (≥ 2; per-model values chưa kiểm here);
- the CHAIR leaderboard used batch 8 (supplementary l.158).

Their files record `parity_slice0`, which is a batch-1 check of the first slice only. C's K1 shows that batched decoding is not batch-invariant: 42/50, 37/50 and 31/50 identical, so 16–38 % of items differ (C_ATTR_DEV_ADDENDUM_v1_2 l.5). That is a separate disclosure item for the paper writer (Q9).

## 2. Models

### 2.1 Final ordered list

Family is read from the language model (plan §4.2 l.181: "read from the pinned config.json/registry LLM base"). The target is the **first four that pass G4 and G5** (§6). An order number is skipped, never a STOP, when its snapshot is missing or a pin differs (rule of C-ATTR §3.2, l.113).

| Order | Key | Hub id @ revision | Licence, gate | Language model | Vision encoder (verify at pin, CC-184 F3) | Params | Weights loaded | Fits on 24 GB at batch 1 | Pins | On hc2 now |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `aya_vision_8b` | `CohereLabs/aya-vision-8b` @ `d7601ac8fd3baf6f59c5fc9514c618ef0f24268f` | cc-by-nc-4.0 + Cohere Labs acceptable-use policy; gated "auto" | Command R7B (cohere2); Vietnamese is one of its 23 listed languages | SigLIP2-so400m-384 | 8.63 B | about 17.3 GB bf16 | yes (C-T1, A-T3, C-ATTR 1b on 3090s) | complete, 13 files, `c_t1_registry.json` 09e6f90a | **yes**, `/root/ncs-data/models/c_t1_aya_vision_8b` (C's tree; read-only reuse via `A_E3_SNAP_aya_vision_8b=/root/ncs-data/models/c_t1_aya_vision_8b`) |
| 2 | `gemma3_4b` | `google/gemma-3-4b-it` @ `093f9f388b31de276ce2de164bdc2081324b9767` | Gemma Terms of Use; gated "manual", accepted by the PI 2026-11-11 (PI-1111h, LOG l.2175; token GET `config.json` HTTP 200) | Gemma 3 (multilingual) | SigLIP so400m (896 px) | 4.30 B | about 8.6 GB bf16 | yes | 13 files in `l1b_registry.json` cd210a7c, **4 null** (two safetensors, `tokenizer.json`, `tokenizer.model`). Fill them only from the Hub API LFS sha256 at this revision, never by hashing fetched files, before the registration commit; the call is named in the registration `statement` (P2; CC-349 ruling 2, W6) | no, fetch |
| 3 | `idefics3_8b` | `HuggingFaceM4/Idefics3-8B-Llama3` @ `fddb4ff79181e55a994674777e06cd5456ce3dc3` | apache-2.0 (card); not gated. Llama 3.1 base licence terms chưa kiểm | Llama 3.1 8B | SigLIP so400m | 8.46 B | about 16.9 GB bf16 | yes (A-T3 batch 2) | complete, 12 files (A-N2 JSON d5714e2b; same pin in l1b) | no, fetch |
| 4 | `llava15_7b` | `llava-hf/llava-1.5-7b-hf` @ `b234b804b114d9e37bb655e11cbbb5f5e971b7a9` | llama2; not gated | Vicuna-7B v1.5 (Llama 2) | CLIP ViT-L/14-336 | 7.06 B | 14.1 GB fp16 (registered dtype float16) | yes (A-N2 batch 8) | complete, 15 files (A-N2 JSON) | no, fetch |
| 5 (fallback) | `smolvlm2_2b` | `HuggingFaceTB/SmolVLM2-2.2B-Instruct` @ `482adb537c021c86670beed01cd58990d01e72e4` | apache-2.0; not gated | SmolLM2 1.7B | SigLIP base-patch16-512 (chưa kiểm) | 2.25 B | 4.5 GB bf16 (9.0 GB on disk) | yes | complete, 14 files (A-N2 JSON) | no, fetch only if needed |
| 6 (fallback) | `llava16_mistral_7b` | `llava-hf/llava-v1.6-mistral-7b-hf` @ `2424fdd47412fccc66d91719126b420e9fbd7065` | apache-2.0; not gated | Mistral-7B-Instruct-v0.2 | CLIP ViT-L/14-336 | 7.57 B | about 15.1 GB bf16 | yes (chưa kiểm on our harness) | **none yet**: every file hash from the public tree API before the registration commit, or the row is dropped | no, fetch only if needed |

The plan's own list (§4.2 l.179) names candidates, not a fixed four: Aya-Vision-8B, Idefics3-8B, LLaVA-1.5-7B, SmolVLM2-2.2B, and "PaliGemma2 or mBLIP". This list keeps the first four in the plan's roles, with these changes:
- Gemma-3-4B-it replaces "PaliGemma2 or mBLIP" and moves to order 2, because it is the only other one with a documented multilingual card.
- SmolVLM2 becomes a fallback (English-only card).
- PaliGemma2 and mBLIP are out: neither ships a chat template, and the harness builds every prompt with `apply_chat_template` (`decode_hf_vlm.py` l.210). Using them would mean new code and a different prompt.

**Expectation (AI opinion):** Idefics3 and LLaVA-1.5 have English-only cards. Idefics3 failed the L1-b floor (CC-186; C-ATTR §3.2 l.105). Either may fail G4. Both fallbacks are also English-first. A realistic outcome is **two to four** models that pass. The arm reports the number reached (S6).

**Already fetched on hc2:** Aya-Vision only. **Fetch needed:** Gemma-3-4B, Idefics3, LLaVA-1.5, and fallbacks only on demand. On a second host, **all** models need a fetch (Aya too; the operator token has Aya access from C-T1, re-check at fetch). Download size for orders 1–4 is about 57 GB.

### 2.2 Excluded, with reason

- **InternVL3-8B-hf** (on hc2). Its language model is Qwen2.5-7B (CC-184 r2, LOG l.854; C-ATTR §3.1 l.95: "Qwen2.5-VL and InternVL3 share the Qwen2.5 language-model line"). The brief calls it an other family. It is another **vision** family, but by the plan's rule it does not count (Q2).
- **Qwen2.5-VL-7B** (on hc2): the paper's own family.
- Every model with a Qwen language model: LLaVA-OV, Vintern (plan l.180).
- **Llama-3.2-11B-Vision**: gate not accepted (PI-1111h).
- **Gemma-3-12B**: about 24.4 GB bf16, does not fit (C-ATTR l.110).
- **InternVL2.5-8B**: needs remote code; the harness forces `trust_remote_code=False`.

### 2.3 Paper wording (CC-184 F3; ruling file `.session_backup/2026-10-30/rulings/CC-184.txt` l.127–133)

The paper never writes "non-Qwen", "non-Qwen-only" or "outside our main Qwen-VL set". It names the models and counts their families. Pre-written sentences, with families verified from each snapshot's `config.json` at the pin (the operator records `text_config.model_type` and `vision_config.model_type`, names only):

- Four pass: "Four further models, Aya-Vision-8B, Gemma-3-4B-it, Idefics3-8B and LLaVA-1.5-7B, span three language-model families (Command R7B; Gemma 3; Llama, in Llama 3.1 and Llama 2 form) and three vision-encoder lines (SigLIP2, SigLIP, CLIP). Idefics3-8B and LLaVA-1.5-7B also appear in the eight-LVLM ladder (A-N2 registry), and Aya-Vision-8B and Idefics3-8B in the COCO arm (A-T3)." No sentence about language-model lineage relative to the Qwen systems is printed (CC-349 Q14): a reworded "non-Qwen" is barred. Naming each language model as read from `config.json` at the pin is enough.
- Three pass: name the three and count again. If Gemma and Aya are two of them, say "two language-model families besides Llama".
- Two pass (Aya, Gemma): "Two further models, Aya-Vision-8B and Gemma-3-4B-it (language models Command R7B and Gemma 3) …". Also say that the other candidates did not write Vietnamese often enough to be scored (G4 counts).

## 3. Prompts and decoding

| Prompt key (`scripts/evaluate.py` PROMPTS, a68d5682) | Part | sha256 of the text | Max new tokens |
|---|---|---|---|
| `short` (the paper's short Vietnamese prompt) | 7a | `8870589c4a32307cbbeb68e363490007682237c0b5a3a1ee7e21cb91fce93886` | 60 |
| `detailed` (the paper's detailed Vietnamese prompt) | 7a | `0addb5dd720e4f24ac912d6fede9cb718e4051bc6944a85d9e7a92b0abb7ed08` | 160 |
| `short_en` | 7b | `0cdbdf77fae4c04bdf4cd626a9eaf9adec5ef0411aac5d816f6c916a69604893` | 60 |
| `detailed_en` | 7b | `525a4e1bf5849e2c38e44cadceed724f66167ac95e621764c384865574913c4a` | 160 |

The four hashes were recomputed today from `evaluate.py` and equal the G2-B registration (c506bc77) and A-N2 (`short_en`, `detailed_en`). The decoder reads each text from `evaluate.py` and refuses a hash mismatch (`decode_qwen3vl.prompt_text`, l.77–85).

**Decoding.** Decoder: `scripts/lb/decode_hf_vlm.py`, sha256 `e2de18811e2ffeb61ed72cb2399d41123e9a8f6ccd73a5ec35f778dcbe2f5ac4`, unchanged since A-N2 (it is A-N2's `decoder.sha256`). Settings:
- `do_sample=False`, `num_beams=1`; everything else from each snapshot's `generation_config.json`, recorded per output;
- first-EOS cut, honouring a list of eos ids;
- `trust_remote_code=False`; sdpa; dtype as registered (bf16, LLaVA-1.5 fp16);
- `processor_kwargs {}`; left padding;
- every image checked against its manifest sha256 before it is decoded;
- venv `venv-lb` (torch 2.5.1+cu121, torchvision 0.20.1+cu121, transformers 4.57.6, accelerate 1.15.0; + num2words 0.5.14). Gemma 3 and Aya-Vision need transformers ≥ 4.50, which holds.

**The only setting chosen here: `batch_size: 1` for every model.** With B = 1 the decoder's `parity_slice0` is empty by design (l.267), and D1 (G5) replaces it.

No code change is needed: batch size, sets, runs and pins are all registration fields of `decode_hf_vlm.py`.

## 4. Files that exist before the judge read (to build; not built by this writer)

| File (all in `manuscript/prereg/2026-11-12_a_e3_arm/` unless named) | Content | How |
|---|---|---|
| `A_E3_REG_v1.json` | schema `vsps.lb_prereg.v1`; `prereg_id` `2026-11-12_a_e3_arm`; `decoder` {path, sha256 e2de1881…}; `venv.packages` as A-N2; `decode.prompts` (4 hashes above); `decode.max_new_tokens` {short 60, detailed 160, short_en 60, detailed_en 160}; `models` in the §2.1 order with `batch_size: 1`, blocks copied byte-for-byte otherwise from A-N2 JSON (idefics3, llava15, smolvlm2), `c_t1_registry.json` (aya), `l1b_registry.json` (gemma, 4 hashes filled), tree API (llava16_mistral); `datasets` {`xm600`: manifest `xm600.tsv`, 600, `image_dir` `xm600`; `xm600f50`: manifest `xm600_f50.tsv`, 50, `image_dir` `xm600`}; `runs`: per model `ae3_<key>_xm600f50-<mode>` and `ae3_<key>_xm600-<mode>` for the four modes (6 × 8 = 48 runs) | coordinator, by a short copy script whose output is diffed against the three sources. Gemma hashes: one authenticated `paths-info` call at the revision with the stored token (never printed), the 4 LFS sha256 written in, and the source call noted in `statement` |
| `xm600.tsv` | 600 rows `id \t id.jpg \t sha256`, in the order of `data/xm3600_subset.txt` (f5ab86c7; sorted ids, = `test_data.json` 0a613214 image ids) | sha256 of each laptop image `data/datasets/xm3600/images/<id>.jpg`, then checked equal to the 600 `image_sha256` values stored in `g2b_q3_xm600-short-T0.preds.json` (the images Paper A decoded). Any difference is a STOP |
| `xm600_f50.tsv` | the first 50 rows of `xm600.tsv`, byte-equal | `head -n 50` |
| `SHA256SUMS_E3` | repo-relative sha256 of: the registration, both manifests, this file, `scripts/a_e3/a_e3_job.sh`, `scripts/lb/decode_hf_vlm.py`, `scripts/g2b/decode_qwen3vl.py` (8a855ef4), `scripts/evaluate.py` (a68d5682), `rescap/vlm/base.py` | `sha256sum` |
| `scripts/a_e3/a_e3_job.sh` | v1 sha256 `afa035bbc26814d8593da95c6b65609596387604fe230158afcc92a9a61de68a` (read in CC-349, Q8); revised for CC-349 W1-W4 and the W7 launch line (`scripts/a_e3/A_E3_JOB_W.diff`); its sha256 is the one in `SHA256SUMS_E3` | – |

## 5. Sets, runs and counts

| Part | Runs per model | Captions per model | Four models |
|---|---|---|---|
| 7a | `xm600f50-short`, `xm600f50-detailed` (G4 + D1), then `xm600-short`, `xm600-detailed` | 100 + 1,200 | **4,800** registered captions + 400 check captions |
| 7b (only models that passed 7a) | the same with `short_en`, `detailed_en` | 100 + 1,200 | **4,800** + 400 |

Images: the 600 of `data/xm3600_subset.txt` only. No other XM3600 image, no reference and no label goes to the host.

## 6. Order, host gates and stop rules

### 6.1 Order

1. **Part 7a first.** Run the models in the §2.1 order. For each model: the two 50-image runs, then G4 on both, then the two 600-image runs, each followed by G5. The part ends at four passing models, the end of the order, or S5.
2. **Pull 7a.** Verify it and make it read-only (§8). This is the hand-over to the labelling top-up (§9).
3. **Part 7b**, only for the models in `passed_7a.txt`, in the same order. GPU idle between parts is about 10 min.

7a goes first because the top-up session needs only the Vietnamese captions.

### 6.2 Host gates

| Gate | Check | Fail |
|---|---|---|
| G0 facts | the `running-rented-gpu-jobs` host facts (nvidia-smi = 1× RTX 3090/3090 Ti 24 GB, lscpu, free, df, 4 GB dd, clock skew < 60 s) | FAULT: delete the host (second host only) |
| G1 tree and pins | sparse clone (§7) at the registration commit; `git diff --quiet HEAD`; `sha256sum -c SHA256SUMS_E3` (in the job); then the custody gate (in the job, W4): no `data/` in the A-E3 tree, `$NCS_DATA/datasets` holds only `xm600`, and that dir holds exactly 600 regular `*.jpg` files and nothing else | STOP |
| G2 self-test | `decode_hf_vlm.py --selftest --prereg A_E3_REG_v1.json` (in the job, every part): registration consistency, 40-hex revisions with file hashes, decoder pin, prompt hashes, snapshot pins, slices/resume, tiny LLaVA batch vs batch-1, determinism, image-sha refusal. Before the first job, the operator also runs `bash -n scripts/a_e3/a_e3_job.sh` on the host. There is no separate dry run: an empty data dir would not stop the job cleanly (the decoder loads the model before the first image check), and the loads would count against the cap. The first model's two 50-image runs are the smoke step | STOP |
| G3 snapshot | `--check-snapshot <key>` against every pinned file | that order number is SKIPPED (S2) |
| G4 language | on each 50-image run: share of captions with a Vietnamese-only letter (ă â đ ê ô ơ ư) or a Vietnamese tone mark after NFD (the definition of `c_attr.py` l.81–83, l.267–272, inlined in the job). 7a: ≥ **0.95** for both Vietnamese prompts (≤ 2 failures of 50; C's threshold). 7b: share of captions with no such mark **and** at least one ASCII letter ≥ 0.95, so an empty caption fails (the 7a definition is unchanged) | the model is NOT VIETNAMESE-ASSESSABLE (7a), or not English-assessable (7b). Its 600-image runs are not decoded, and the next order number runs (7a). Its 50-image outputs decoded so far are kept and counted |
| G5 D1 determinism | after each 600-image run: its first 50 captions equal, as strings, the 50-image run's 50 captions (two separate model loads, batch size 1). Must be **50/50** | the model's outputs are HELD: never handed to labelling or scoring without a judge line, and the model is not in `passed_*.txt`. 7a continues with the next order number (S4) |
| G6 cap | before each 600-image run: spent seconds (all runs, both parts, model loads included) + 600 × (that model's 50-image seconds / 50) ≤ 36,000 s. Also, before every attempt of any run (50- or 600-image), its timeout is cut to 36,000 s − spent | CAP STOP: that run and all later runs are NOT RUN (S5). A run killed by the cut keeps its partial file and is reported NOT RUN |

The checks print counts and shares only. No caption text is printed or logged.

### 6.3 Stop rules

- **S1 (tree, pins, self-test).** A failed G1 or G2 stops the job before any decode. A fix needs a new commit and a one-judge read.
- **S2 (model skipped).** A missing or changed snapshot, or a G4 failure, skips the model. This is not a STOP.
- **S3 (decode failure).** One resume attempt per run (the decoder resumes from its partial file). A second failure (OOM, exception, timeout) is a MODEL FAIL: the model's remaining runs are NOT RUN and the next order number runs. Timeouts: 1,800 s for a 50-image run; max(1,800 s, 2 × projected) for a 600-image run; each is cut to the cap remaining (S5).
- **S4 (D1).** As G5. Two D1 failures in a part also stop that part, because a host-level cause is likely. The job counts them per part and at the second logs `PART STOP: two D1 failures (S4)`. Then pull, and send to the judge.
- **S5 (cap).** One hard cap of 10 GPU-h (36,000 s) over 7a + 7b together (PI-1105k). 7a runs first, so it gets priority.
  - The plan's split (7a 6 GPU-h, 7b 4 GPU-h) is a projection, not a stop (Q1).
  - The cap is hard: before each attempt of every run, 50- or 600-image, the job cuts the timeout to `CAP_S − spent`. A run killed by that cut, or one with no cap left, logs `CAP STOP at <run>`, its partial file is kept, and it and every later run are NOT RUN.
  - The cap cuts in the registered order, so 7b's last models go first.
  - The PI line (§12) is asked only if a 7b CAP STOP actually happens, or at `JOB DONE 7a` if spent_7a + the 7b projection (from the 7a 50-image rates) exceeds 36,000 s.
- **S6 (fewer models).** If fewer than four models pass 7a, the number reached is reported. Fewer than two passing models means the arm adds no family comparison. It is then reported as such and no Annex B slope row is printed.
- **S7 (host).** No job runs while `/root/outputs/c_attr_b1/RUNNING` exists or another GPU process is present (job pre-checks; CC-346 R5).
  - On a restart on the same host, a run whose `.preds.json` exists is never decoded again. An unfinished run resumes from its partial file. The ledger sums every attempt of a run, both for the rate and for the cap.
  - On host loss, a re-rental needs a short machine-loss addendum with a one-judge read.
- **S8 (no scoring on the host).** No score, no reading of caption text, and no `xm3600_oiv7.py` on the host.

## 7. Host, layout and custody

**Host: hc2 (machine id `h1`), CC-349 ruling 3 (Q5).** HC3 is gone, and PI-1112b bars an idle rented GPU.
- hc2 runs C block 1b. Projected end is about 14:05–14:45 VN today, with a cap stop at about 20:00 VN at the latest (LOG l.2225).
- A-E3 decodes start only when all of these hold: block 1b shows JOB DONE and its RUNNING file is gone; the 1b outputs are pulled, verified against their SHA256SUMS and made 444, with the OPS line written; the round-2 diff read (CC-349r2) and the commit are done.
- If the round-2 read and the commit are not done when the 1b pull is verified, the arm is not staged and PI-1112b applies at once (pull, verify, delete the host), unless the PI answers CC-349's conditional question otherwise.
- C's scoring stages may run CPU-only under `nice -n 19` beside the A-E3 decodes (CC-348 (b), cited in CC-349 ruling 3(b)). One OPS DEVIATION line gives the start and end of every C stage that runs beside A-E3. The A-E3 start line records `free -g` and `df -BG /root`. No C decode job (block 2) starts while `/root/a_e3/out/RUNNING` exists.
- Staging while 1b decodes (CC-349 ruling 3(c), a recorded narrow overrule of CC-346 ruling 6 / R5): network, disk and light hashing only, no model load, no GPU, no decode; every command under `nice -n 19 ionice -c3`, one model at a time; `df -BG /root` shows at least 100 G before the first fetch and at least 40 G after it; nothing under `/root/ncs-data`, `/root/outputs` or the HF hub cache (`HF_HOME=/root/a_e3/hf`, fetch with `/root/venv-lb/bin/python`); no archive left on disk; one OPS DEVIATION line per item. These fetches are unverified staging; the only pin check is G3 under the committed registration.

**Layout (hc2):**
- Code: a sparse, code-only clone at the registration commit in `/root/a_e3/vsps`. `git clone --filter=blob:none --sparse` plus `git sparse-checkout set --no-cone /scripts/a_e3/ /scripts/lb/ /scripts/g2b/decode_qwen3vl.py /scripts/evaluate.py /rescap/ /manuscript/prereg/2026-11-12_a_e3_arm/`.
  - A full clone is **not** allowed: `data/xm3600/oiv7_labels.json` and `vi_oiv7_map.json` are git-tracked, which makes them the label gold.
  - Note for the judge: hc2's `/root/vsps` is a full clone and already holds these two tracked files. The A-E3 job never reads them.
- Images: tmpfs `/dev/shm/a_e3/datasets/xm600/` (mode 700), so `NCS_DATA=/dev/shm/a_e3`.
  - The push follows the skill: six streams, `sha256sum -c` against `xm600.tsv`, count = 600, no links.
  - Never under C's `$NCS_DATA/datasets`, because C's guard allow-lists that dir (`c_attr.py` l.771, `ISO_DATASETS`).
- Models: `/root/a_e3/models/<key>`.
  - Fetch with `HF_HUB_OFFLINE=0 $PY scripts/lb/decode_hf_vlm.py --prereg … --fetch <key> --snapshot /root/a_e3/models/<key>`.
  - The token goes only through stdin into the fetch shell's environment; it is never printed and never in a file in the tree.
  - On hc2, Aya is reused read-only from C's tree via `A_E3_SNAP_aya_vision_8b=/root/ncs-data/models/c_t1_aya_vision_8b` (a literal path: the job sets `NCS_DATA=/dev/shm/a_e3`, so `$NCS_DATA/models/...` would be a missing dir and Aya would be skipped).
  - Fetch orders 2–5 before 7a starts (SmolVLM2 is 9 GB and waits until needed if `df` does not allow it, CC-349 ruling 3(c)), so that a G4 failure falls through to the next order without an operator. Order 6 is fetched only if its pins are in the registration commit.
- Outputs: `/root/a_e3/out/`. Machine id from `/root/.vsps_machine_id`.

**Custody.**
- No gold in the A-E3 tree, its data dir or its outputs: no human label, no `key.json` or `assignment.json`, no OIV7 labels or class map, no XM3600 references. On hc2, C's full clone `/root/vsps` holds the tracked `data/xm3600/oiv7_labels.json` and `vi_oiv7_map.json`, and C's dev datasets (including XM-dev500, disjoint from the 600, as is XM-test2500: 0/0 ids). The A-E3 job reads none of them. The job's custody gate (§6.2 G1) stops if the A-E3 tree has a `data/` dir or `$NCS_DATA/datasets` holds anything but the 600 images.
- Only the 600 images, the prompts and the snapshots.
- The images are public Open Images photos (CC BY 2.0). The same 600 were decoded on rented hosts before (O-2293440, O-2308428). The C precedent applies (PI-1104af: a dedicated single-tenant 3090, isolated tmpfs, logged pixel deletion).
- At the end: `rm -rf /dev/shm/a_e3`, logged with the file count before deletion.

## 8. Pull, verify, read-only

1. After `JOB DONE 7a` (the job's last line; `RUNNING` gone), pull `/root/a_e3/out/` to `.session_backup/machines/AE3/root/a_e3/out/` (or `…/ATTR_H1/root/a_e3/out/` on hc2) with `rsync -a`. Never use `--delete`.
2. Locally run `sha256sum -c SHA256SUMS_7a`: all OK. Every `.preds.json` also matches its `.sha256` sidecar.
   - `job.log` is not in the sums. It is written after them, which avoids the C block-1 mismatch (LOG l.2213).
   - A whole-tree digest equal to the host's is logged.
3. `chmod -R a-w` (444). One OPS line: the counts, the `passed_7a.txt` list, `gpu_s`, G4 shares, D1 counts, per-run `hit_max` counts (the sum of each output's `hit_max` values; a count only), and the sha of `SHA256SUMS_7a`.
4. Then start 7b. After 7b, repeat with `SHA256SUMS_7b`.
   - `ledger.tsv` and `checks.log` grow in 7b, so the 7a sums verify only on the 7a pull copy, which is the copy of record.
5. End: wipe the tmpfs (logged), delete hc2 when no approved job remains on it (PI-1112b), do L-after, write the hand-off OPS line.

No output is opened, displayed or scored before the relevant annex is committed. The builder in §9 reads caption text inside code only and prints counts.

## 9. Hand-over to the labelling top-up (plan XM600_GOLD_COMPLETION_PLAN_v1_1 §6)

### 9.1 Why a wrapper, not an edit

`tools/obj_rater/build_assignment.py` (497e5747) is pinned in the labelling plan §8. `a_cert.py` imports its `load_systems`, and `a_cert gate` reproduces its counts (A-CERT §11, l.257–259). Editing it changes a pin that the certification freeze depends on.

The minimal change is therefore a **new** file, `tools/obj_rater/build_topup.py`, that imports the builder unchanged. It is described here and not implemented. It needs its own one-judge code read, and it can be written and read while 7a decodes.

What `build_topup.py --out ~/vsps_labels/xm600_gold_topup1 --name topup1 --extra <files…>` does:

1. **Rebuild the base and prove it.** Call `build_assignment.build(tmp)` with `tmp = <out>/_base` (under `~/vsps_labels`, never `/mnt`). Require `BUILD.json outputs_sha256` equal to the pinned four: assignment `55e07337…`, key `a2cef894…`, practice `e0ed805b…`, overlap `4f971966…`. Otherwise STOP.
   - The wrapper code (never a person) reads `_base/key.json` in memory for the base roles (foils, repeats, part-1 targets). It then deletes `_base`, and the deletion is logged.
2. **Base named set.** Recompute it exactly as `build()` l.58–79 does, from `load_systems()` (the 12 stored sets) and the Vietnamese references. `key.json` lists only asked pairs, so it cannot give this set.
3. **New systems.** Read the `--extra` files: the LB schema, key `predictions`, all 600 ids required. They are only the 600-image Vietnamese runs (`ae3_<key>_xm600-{short,detailed}.preds.json`) of models in `passed_7a.txt`, from the pulled 444 copy. Then compute `named_new` = pairs that the new systems name **minus** the base named set.
4. **Items, same buckets and wording as the base.**

| Part | Content |
|---|---|
| 1 | new `unknown` pairs (role `target`); new named `absent` pairs (`ctrl_absent`); `ctrl_present` sampled from new named-present pairs, n = round(200 · t1 / 1,790); unnamed-absent foils, n = round(100 · t1 / 1,790), drawn excluding base foils and every named pair; **50 base part-1 targets** asked again (`old_repeat`, hidden among part-1 screens) |
| 2 | new `unmapped` pairs (`target`) |
| 3 | repeats of new part-1 targets, n = round(150 · t1 / 1,790) |

   - t1 = number of new part-1 targets.
   - CC-327 L2: pairs of `tranh`, `bức tranh`, `mỏm đá` that Open Images marks absent never become controls or foils (Q6).
5. **Seeds, ids, overlap.**
   - rng `random.Random(f"{SEED}|topup1")`.
   - qid = `sha256(f"{SEED}|topup1|{part}|{image}|{class}")[:12]`, asserted disjoint from every base qid.
   - Screen ids are prefixed `topup1-`.
   - `practice.json` is copied byte-equal.
   - `overlap_images_topup1.txt` = base `overlap_images.txt` ∩ images with a top-up target, so the second annotator keeps the same 150 images.
6. **Outputs** to `--out`: `assignment.json`, `practice.json`, `key.json` (private, not served), `overlap_images_topup1.txt`, and `BUILD_TOPUP1.json` (counts by part and role, input sha256 including every `--extra` file and the base check). No caption text is written. A copy of all except `key.json` goes to `manuscript/prereg/2026-11-12_a_e3_arm/topup1/`, as for the base.

**Command after the code read and the 7a pull** (laptop, as the base build: the builder reads the Open Images labels, which never go to a host):

```
NCS_DATA=data ~/.venvs/c_stage1_lists/bin/python -B tools/obj_rater/build_topup.py --out ~/vsps_labels/xm600_gold_topup1 --name topup1 \
  --extra $(sed 's#^#.session_backup/machines/AE3/root/a_e3/out/ae3_#; s#$#_xm600-short.preds.json#' .session_backup/machines/AE3/root/a_e3/out/passed_7a.txt) \
          $(sed 's#^#.session_backup/machines/AE3/root/a_e3/out/ae3_#; s#$#_xm600-detailed.preds.json#' .session_backup/machines/AE3/root/a_e3/out/passed_7a.txt)
python3 -B tools/obj_rater/server.py --dir ~/vsps_labels/xm600_gold_topup1 --annotator PI --port 8791
```

On hc2 the pull copy is `.session_backup/machines/ATTR_H1/root/a_e3/out/` (§8 step 1); the command then uses that path in place of `machines/AE3`. The server, page and wording are unchanged. The labels go to `~/vsps_labels/xm600_gold_topup1/labels_PI.jsonl`, separate from part 1. Session-end LOG lines follow plan §3.

### 9.2 How the top-up stays blind
- The page shows the image, the class and the hint. It shows no caption, no system name and no role.
- Targets, controls, foils and `old_repeat` items are mixed within screens. Screen order and question order are random with the fixed seed.
- **Disclosed leak:** the annotator knows that a top-up session asks about pairs named by new models, so that group is not blind. Which of the new models named a pair is still hidden. The 50 old repeats and the controls dilute the group, and they also give a cross-session test-retest figure.
- The PI has already seen these images in part 1. Disclose this beside the top-up results.

### 9.3 Expected size and time (rough arithmetic, AI opinion; not computed on any output)
- Base: 12 caption sets + references name 4,910 pairs on 600 images (8.2 per image). Of these, 3,890 (79 %) are unsettled (1,790 part 1 + 2,100 part 2).
- Assumption: each new model adds 0.4–0.8 pairs per image beyond the base, with about 30 % overlap between models. Four models then give about 1.1–2.2 new pairs per image, so **650–1,350 new named pairs**, of which about **500–1,050 targets**.
- Questions, with controls, repeats and the 50 old repeats: about **650–1,350**.
- At 5–8 s per question, that is **about 1–3 hours of labelling**. With two passing models, roughly half.
- The PI's own rate is not measured: only line counts may be read (345 answers on 11-11).
- The exact counts are printed by the wrapper before the session starts.

**Timing (VN time, estimate).**
1. Round-2 diff read and commit before 07:00Z (14:00 VN).
2. C block 1b ends, is pulled and verified about 14:00–14:45; 7a starts on hc2 right after.
3. 7a finished about 19:30–23:30 (§10: 3.7–7.6 GPU-h).
4. Pull, build and code-read top-up ready about 1 h later.

### 9.4 Which analyses may use the top-up labels
- **By construction, no top-up target pair is named by any of the twelve stored caption sets or by a reference.** So it lies outside every registered H1–H3 universe of A-CERT v1.1 (H3 `N_u` = "named by at least one of the twelve caption sets", l.196; H2b over the twelve systems, l.188).
- The only registered home is A-CERT §10, row "Other-family arm …: development; C-ref and C-label at once; completed-gold rows only after a top-up labelling session and a separate unsealing; CC-327 L2 applies" (l.247), and §12 step 7 ("separate, later unsealings … never change a part-1 verdict").
- That row fixes no statistic, so **a short addendum is needed** (Annex A). It must be judge-read and committed before any top-up label value is opened. Until then, top-up labels enter no analysis.
- They never enter gold (ii) for the twelve systems' rows: the registered rows use the base session's labels only.

## 10. GPU-hour projection (RTX 3090, batch size 1)

Measured rates, with sources:

| Source | Batch | Rate per caption |
|---|---|---|
| G2-B Qwen3-VL-8B on **these 600 images**: short T0 1,037 s / 600; detailed T0 6,159 s / 600 (599 of 600 at the 160 cap). From `started_utc`/`finished_utc` of the stored files | 1 | **1.73 s / 10.27 s** |
| A-T3 Aya-Vision tier 2, COCO English (plan §4.3, LOG l.932) | 2 | 1.5 s / 3.7 s |
| C-ATTR 1b D1 on hc2, Aya-Vision, Vietnamese ICL captions (LOG l.2224) | 1 | 1.40 s (load excluded) |

Projection for 7a. The low end uses the A-T3-like rates; the high end assumes every 8B model is as slow as Qwen3-VL on these images.

| Model | Short s/cap | Detailed s/cap | 600-image runs | 50-image checks + loads | GPU-h |
|---|---|---|---|---|---|
| Aya-Vision-8B | 1.5–1.8 | 3.7–10.3 | 0.87–2.0 h | 0.1–0.2 h | 1.0–2.2 |
| Gemma-3-4B | 0.8–1.2 | 2.5–6.0 | 0.55–1.2 h | 0.1 h | 0.6–1.3 |
| Idefics3-8B | 2.0–2.5 | 4.5–10.3 | 1.1–2.1 h | 0.1–0.2 h | 1.2–2.3 |
| LLaVA-1.5-7B | 1.0–1.5 | 3.5–8.0 | 0.75–1.6 h | 0.1–0.2 h | 0.85–1.8 |
| **7a total** | | | | | **3.7–7.6 (point about 5)** |
| **7b total** (English is shorter in tokens) | | | | | **3.0–6.0 (point about 4)** |

- The plan's 4.0 + 3.3 = 7.3 GPU-h is likely low, because the plan rates were from batched English decodes.
- At the point values, 7a + 7b ≈ 9 GPU-h, inside 10. At the high end, 7a alone is about 7.6 and 7b is cut by S5 to about 2.4 GPU-h, roughly one or two models.
- Wall time for 7a ≈ its GPU-h (one GPU, sequential), so the earliest finish is about 19:30 VN on hc2 (§9.3).
- Money: about 9,300 VND/h (PI-1104af scale) × (3 h setup + up to 10 h + 1 h) ≈ 130k VND, which is not a constraint (PI 11-10). Before renting, run the L-before check of the skill.

## 11. Descriptive rows on existing golds (Annex B, summary)

Annex B binds only if committed before the 7a pull is opened by anyone. Scoring is not part of this run.

## 12. Open questions for the judge

| # | Question | Recommended answer |
|---|---|---|
| Q1 | One hard cap of 10 GPU-h over 7a + 7b, with 7a first, instead of the plan's per-part caps 6 / 4? | Yes. The PI's number is 10 in total, and 7a feeds the labelling and the paper's Vietnamese claim. The plan split stays as a projection. |
| Q2 | The brief calls InternVL3 an other family. Its language model is Qwen2.5 (CC-184 r2). Include it? | No. Follow the plan's language-model rule. If a fifth row is wanted, label it "InternViT encoder, Qwen2.5 language model", count it with the paper's language-model family, and keep it out of the four. |
| Q3 | Model list and order (§2.1): Gemma-3-4B replaces "PaliGemma2 or mBLIP"; SmolVLM2 becomes a fallback; LLaVA-1.6-Mistral is fallback 6 with pins still to fill. | Accept. Drop order 6 if its pins are not in the registration commit. |
| Q4 | G4 threshold 0.95 per Vietnamese prompt on 50 captions (C's rule), and G5 D1 = 50/50 per run with outputs HELD on failure. | Accept both. G4 is a language gate only, not a quality gate, which is why a fluent-but-poor model still enters. |
| Q5 | Host: a second 3090 now (`ae3`), or hc2 after C 1b ends? | CC-349: hc2 (ruling 3), not a second host; the recommendation was overruled on the changed facts (HC3 gone, PI-1112b). |
| Q6 | CC-327 L2 for the top-up: `tranh`, `bức tranh`, `mỏm đá` with Open Images "absent". | Exclude them from controls and foils, and do not ask them. Their registered status stays (Open Images is never overridden, plan §5). The excluded count is printed. |
| Q7 | Top-up composition: the 50 `old_repeat` items and the scaled controls (§9.1 step 4). | Accept. They dilute the group leak and measure cross-session agreement. Their answers are never labels. |
| Q8 | A job script was written (`scripts/a_e3/a_e3_job.sh`). It is an adaptation of `lb_a_n2_decode.sh`, plus G4/G5/G6 as inline checks; the decoder is unchanged. | Read it as code in this round. CC-349: there is no separate dry run; the host check is `bash -n`, G2 inside the job, and the first model's 50-image runs as the smoke step. |
| Q9 | The A-N2 ladder, A-T3 and the CHAIR leaderboard were decoded batched. Does Paper A need a batch disclosure for them? | Yes, one supplement sentence per arm: batch size, the `parity_slice0` count where it exists, and C's K1 numbers as the known size of the effect. That is a paper-writer item, not part of this run. |
| Q10 | Part 7b: the supplement says there is no English-to-Open-Images class map (l.297), and the L2-P1 owner check (plan step 7, §3.1) is open. | Decode 7b in this rental, as the PI approved. Score it only on the English reference-gold ladder (Annex B). No Vietnamese-versus-English gap claim until the owner check. |
| Q11 | One top-up session after all of 7a, or a first top-up from the first two passing models? | CC-349: one session after all of 7a. The 18:00 VN split (topup1/topup2) is not licensed; it may be added only in the build_topup read, with a mid-run pull rule. |
| Q12 | The custody line for XM3600 images on a rented host (PORTFOLIO_STRATEGY_writer2 Q4) has no logged answer. | Covered by PI-1105k/PI-1107c (an arm "on XM3600-600" on a rented 3090) and the precedents in §7. No PI line is needed. If the judge disagrees, it becomes the PI line below. |

| Q13 | The short cap is 60 new tokens (the second backbone's). The first family's short cap is chưa kiểm (evaluate.py default 160; job file missing), and its pixel bounds differ from each new model's defaults. | Keep 60/160 and the defaults. Disclose them as harness differences (§1), and report per-run `hit_max` counts at the pull. |
| Q14 | CC-184 F3 bars "non-Qwen" and "outside our main Qwen-VL set". May the paper say that none of the four uses a Qwen language model, once this is verified from `config.json`? | CC-349: no. Name each language model as read from `config.json` at the pin (Command R7B, Gemma 3, Llama 3.1, Llama 2); naming them is enough. |

**CC-349 answers (§6 of the ruling):** Q1 yes, one hard 10 GPU-h cap over 7a + 7b, 7a first, the 6/4 split a projection only. Q2 no, InternVL3 out, no fifth row. Q3 accept; order 6 dropped unless its pins are committed. Q4 accept; 7b gets the W3 fix. Q5 hc2. Q6 accept. Q7 accept in principle, bound in the build_topup read and addendum E3. Q8 accept after W1-W4, no separate dry run. Q9 yes, a writer item. Q10 decode 7b, score it on the English reference ladder only, no gap claim. Q11 one session after all of 7a. Q12 covered, no PI line. Q13 keep 60/160 and the defaults, disclose, log hit_max counts. Q14 no lineage sentence.

**PI line (only if needed; CC-349 ruling 4):** asked only if a 7b CAP STOP actually happens, or at `JOB DONE 7a` if spent_7a + the 7b projection exceeds 36,000 s: may the cap rise from 10 to 14 GPU-h for 7b only? Recommended: yes (money is not a constraint, PI 11-10). Default if the PI is silent: 7b keeps what fits under 10, and the rest is NOT RUN.

---

## Annex A. Draft addendum to A-CERT v1.1 for the top-up labels (to be judge-read and committed before any top-up label is opened)

**A-CERT addendum E3 v1 (draft).**
- **Scope.** The other-family row of §10. Systems S_E = the 600-image Vietnamese caption sets of the A-E3 models that passed G4 and G5 (two per model), on I600.
- **Label.** "development; new decodes on previously analysed images; new labels; single annotator until the second annotator's top-up overlap is labelled".
- **No verdict** attaches to any row.

1. **Freeze E3, before the top-up labels are opened.**
   - `a_cert.py freeze` logic is run on the 12 + |S_E| caption sets, and FREEZE_E3.json is pinned in the LOG.
   - It holds the C-ref certificates of every pair of systems with at least one member in S_E, the budgets β(N_s; w) and the §4.4 low ends for S_E.
   - The 12-system FREEZE (c51ea7dc) is unchanged and keeps binding every part-1 row.
   - The code change this needs is in `a_cert.py` only: an optional list of extra caption files, added after its unchanged call of `build_assignment.load_systems()`, never by default. It gets a one-judge code read, and the 12-system `gate` must still reproduce its registered numbers.
2. **Completed status for S_E** is the plan §5 rule, extended:
   - base labels (part 1 last line wins) for base pairs;
   - top-up labels for top-up pairs;
   - Open Images never overridden;
   - U and A to the remainder;
   - no propagation;
   - `old_repeat` and part-3 answers used only for agreement.
3. **Rows (descriptive):**
   - (E1) completed precision `P_c` on mapped classes per system in S_E, with the image bootstrap as registered;
   - (E2) the H2a counts `V_c`, `V_n` and their interval for certified pairs with a member in S_E, cross-family pairs printed apart;
   - (E3) H2b budget coverage per system in S_E (covered or not), plus the count;
   - (E4) H3 on the universe `N_u'` = pairs named by any of the 12 + S_E sets, with no Open Images status;
   - (E5) per A-E3 model, the completed label-gold slope over its two prompts (two points; printed as a difference, not a slope claim);
   - (E6) cross-session agreement on the `old_repeat` items, and the top-up control agreement, reported whatever its value.
4. **Order.**
   - The part-1 unsealing (A-CERT §12 step 5) comes first.
   - Then the top-up session ends, with its LOG line: `wc -l`, sha256 and a 444 copy.
   - Then a single scoring run on that copy, with the fault rule of §12 step 5.
   - Then a one-judge result read.
   - Part-2 top-up targets follow the part-2 kappa rule; part-1 top-up targets follow the part-1 kappa rule, using the second annotator's labels on `overlap_images_topup1.txt`.
5. **Never:** a top-up label changes a registered H1–H3 verdict or gold (ii) of the twelve systems.

## Annex B. Descriptive rows on existing golds (no labels; summary for a separate one-page scoring note)

- **7a.** Per system: the paper's existing XM3600 measures on the A-E3 Vietnamese files, computed by `scripts/xm3600_oiv7.py score`. These are reference P/R/F1 against refs ∩ OIV7, verified precision, verified-negative hallucination and hit-max share.
  - The scorer reads flat `{id: caption}` files (l.232–238), so the scoring note must name a one-line flattening of `predictions` and log the flat files' sha.
  - Per model, the short-to-detailed difference beside the paper's two families.
  - Label: DEVELOPMENT / A-E3, descriptive, new decodes on previously analysed images.
- **7b.** The English reference-gold ladder only (XM3600-en references, `chair_en`, COCO-80 classes), as the plan's "CPU ladder with XM3600-en reference gold". There is no Open Images English map and no Vietnamese-versus-English gap claim (Q10).
- **Where scoring runs:** the scorer reads the Open Images labels (gold). Under §7 custody these stay off the hosts, which conflicts with the laptop rule of PI-1111 (scoring on the rented host). The scoring note must settle this. Recommended: laptop, as for every earlier XM3600 score, with a deviation line.
