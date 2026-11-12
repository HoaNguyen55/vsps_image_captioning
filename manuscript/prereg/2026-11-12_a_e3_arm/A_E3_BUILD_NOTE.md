# A-E3 build note (prerequisite files of run document v1.1 §4)

Built 2026-11-12T02:14–03:05Z (09:14–10:05 VN) by a builder agent. Nothing was decoded, downloaded to the laptop, committed or logged. No caption text and nothing under `~/vsps_labels/` was opened. "chưa kiểm" = not checked.

**Aligned with:**
- `A_E3_ARM_RUN_DOC_v1_1.md`, sha256 1df371cc…
- `scripts/a_e3/a_e3_job.sh`, sha256 b11a9f6b…
- CC-349 (bb7b93da…), W6.

## Files

| File | sha256 |
|---|---|
| `A_E3_REG_v1.json` | `26c677a2b4d50a02900b0526c98a85bd2dc326e76d5fd30995ae83f9ff0120b2` |
| `xm600.tsv` | `d414e04edb097e4ab850f3189c15ceb5c37753e313bb4d58bcb60c0bb9e6ea33` |
| `xm600_f50.tsv` | `a455a816272c34e45a16a06e26a2067fbb7c26f86674e208eb147973f21874ec` |
| `SHA256SUMS_E3` | `b2b9aa81c1c2462fe6d39e5d926900c1e7f4713b1288deba5232f4d1ca8134dc` |

`SHA256SUMS_E3` covers:
- run document v1.1 (1df371cc), and v1 (f0a375fb) as a record;
- the registration and both manifests;
- `scripts/a_e3/a_e3_job.sh` (b11a9f6b);
- `scripts/lb/decode_hf_vlm.py` (e2de1881), `scripts/g2b/decode_qwen3vl.py` (8a855ef4), `scripts/evaluate.py` (a68d5682), `rescap/vlm/base.py` (e8fee5bc).

`sha256sum -c` passes from the repo root. The name is the one job l.40 (G1) reads.

## Where each value came from

| Value | Source |
|---|---|
| `aya_vision_8b` block | `c_t1_registry.json` (09e6f90a) `models.aya_vision_8b`, copied by script. Only `batch_size` changes, 2 → 1 |
| `gemma3_4b` block | `l1b_registry.json` (cd210a7c) `models.gemma3_4b`. `batch_size` 8 → 1, and the 4 null hashes are filled (below) |
| `idefics3_8b`, `llava15_7b`, `smolvlm2_2b` blocks | A-N2 JSON (d5714e2b) `models.*`, with `batch_size` → 1. The Idefics3 files equal the L1-b files |
| `llava16_mistral_7b` block | new, from the HF API (below). 15 files: every file except `README.md` and `.gitattributes`. All are pinned, so order 6 stays (CC-349 Q3/W6) |
| `venv` | A-N2 `venv`, verbatim (4 packages + `add_only` num2words) |
| `decoder` | path + A-N2 `decoder.sha256`, which equals the file today |
| `decode.prompts` | G2-B registration (c506bc77) `decode.prompts.*.text_sha256`. `short_en` and `detailed_en` equal A-N2. The decoder's `load_prereg` re-checked all four against `scripts/evaluate.py` |
| `decode.max_new_tokens` | 60/160/60/160, equal to G2-B |
| `decode.loader/message/greedy/text` | A-N2 strings, verbatim. A-N2's `batching` string was replaced, because it is false at B = 1 |
| Manifests | Ids come from `data/xm3600_subset.txt` (f5ab86c7). They equal the 600 ids of `test_data.json` (0a613214), sorted, with `filename` = `<id>.jpg`. Each row's sha256 is of the laptop image `data/datasets/xm3600/images/<id>.jpg`; **600/600 equal** the `image_sha256` map of `g2b_q3_xm600-short-T0.preds.json` (82b6ef5f, O-2308428). Only that key was read, in code, counts only. `xm600_f50.tsv` is byte-equal to `head -n 50 xm600.tsv` |

**Copied-block check (after the last edit):** every copied block is diff-equal to its source except `batch_size`. Gemma also differs in its 4 filled hashes, which are the only differing files.

**HF API calls.** All used the generic client `vsps-research-client/1.0` with no e-mail and returned HTTP 200. Responses are kept in the session scratchpad only.

| Model | Call | Auth | UTC | Response sha256 |
|---|---|---|---|---|
| gemma3_4b (W6) | `POST /api/models/google/gemma-3-4b-it/paths-info/093f9f38…` with the 4 paths | token header read from its file in the command, never printed | 03:01:37Z | `0eb3de43…` |
| gemma3_4b | `GET /api/models/google/gemma-3-4b-it/tree/093f9f38…?recursive=1` | same | 02:14Z | `4ab4476d…` |
| aya_vision_8b | `GET …/CohereLabs/aya-vision-8b/tree/d7601ac8…?recursive=1` | same | 02:14Z | `01d9b609…` |
| idefics3_8b | `GET …/HuggingFaceM4/Idefics3-8B-Llama3/tree/fddb4ff7…?recursive=1` | none | 02:14Z | `61b33af5…` |
| llava15_7b | `GET …/llava-hf/llava-1.5-7b-hf/tree/b234b804…?recursive=1` | none | 02:14Z | `5894b5e0…`, byte-equal to A-N2's stored `tree_sha256` |
| smolvlm2_2b | `GET …/HuggingFaceTB/SmolVLM2-2.2B-Instruct/tree/482adb53…?recursive=1` | none | 02:14Z | `92848655…` |
| llava16_mistral_7b | `GET …/llava-hf/llava-v1.6-mistral-7b-hf/tree/2424fdd4…?recursive=1`, and `/revision/2424fdd4…` (info) | none | 02:14Z | `8fdf2043…`; info `a24a2154…` |

- **Gemma, W6:** the four `lfs.oid` values from **paths-info** are identical to the tree-API values and to the JSON:
  - `model-00001-of-00002.safetensors` eb5fd5e9…
  - `model-00002-of-00002.safetensors` fdde0e5a…
  - `tokenizer.json` 4667f208…
  - `tokenizer.model` 1299c11d…

  No fetched file was hashed. The paths-info call is named in `statement`.
- **Cross-check:** all 63 copied pins equal the tree API at their revisions: Aya 13, Gemma 9 non-null, Idefics3 12, LLaVA-1.5 15, SmolVLM2 14. There is no difference.

## Pinned file counts

| Model | Pinned files |
|---|---|
| aya_vision_8b | 13 |
| gemma3_4b | 13 |
| idefics3_8b | 12 |
| llava15_7b | 15 |
| smolvlm2_2b | 14 |
| llava16_mistral_7b | 15 |

The JSON lists the models in the §2.1 order. `--models` prints that order, and the job follows it. There are 6 × 8 = 48 runs.

## Consistency with v1.1 and the job b11a9f6b

- The JSON holds no cap, host, snapshot path or tree path, so the following v1.1 settings live in the job and the launch line, not in the registration:
  - the single 10 GPU-h cap with 7a first;
  - hc2;
  - the Aya path `/root/ncs-data/models/c_t1_aya_vision_8b`.
- `batch_size` is 1 for all six models.
- The run ids equal the job's `ae3_${M}_xm600f50-$m` and `ae3_${M}_xm600-$m` patterns.
- `image_dir` is `xm600`, which matches the job's W4 custody gate (`$NCS_DATA/datasets` holds only `xm600`, with 600 `*.jpg`).
- The S4 part stop, missing in job v1, is coded in b11a9f6b (`d1f` counter).

## chưa kiểm and deviations

- The 4 Gemma hashes and all 15 LLaVA-1.6 pins come from the API only. The host's `--check-snapshot` after the fetch is the first file-level check.
- LLaVA-1.6-Mistral has never been loaded on this harness (chat template, Auto-class resolution at transformers 4.57.6).
- LLaVA-1.6 dtype is registered as `bfloat16`, as v1.1 fixes (§3; §2.1 row 6). The checkpoint is **F16** (API `safetensors.parameters`). SmolVLM2 (F32 checkpoint, bf16 registered) is the precedent.
- v1.1 §4 shows the manifests by bare name (`xm600.tsv`). The decoder resolves `ROOT / manifest.path`, so the JSON holds `manuscript/prereg/2026-11-12_a_e3_arm/xm600.tsv`, and the same for f50.
- The builder brief asked for `SHA256SUMS_A_E3`. The job (l.40) and v1.1 read `SHA256SUMS_E3`, so that name was built.
- Inherited `role` texts are kept byte-for-byte and are now stale. Gemma's says its hashes are null and the gate is pending; Aya's says "non-Qwen LM". They are registration text, not paper text (CC-184 F3 applies to the paper).
- The 600 images were read twice. The first niced pass aborted on a script bug before anything was written, and the re-run was also niced.
- `SHA256SUMS_E3` pins v1.1 and job b11a9f6b. Any further edit to either means rebuilding the sums file.
- `decode_hf_vlm.py --selftest` was not run, because it builds and decodes a tiny model (laptop rule). These checks were run instead:
  - `load_prereg`;
  - `manifest_items` on both sets;
  - `--models`;
  - `--list-runs` (48);
  - `bash -n` on job b11a9f6b.

## Round-2 checklist

- [ ] `schema` = `vsps.lb_prereg.v1`, `prereg_id` = `2026-11-12_a_e3_arm` (§4)
- [ ] `statement` names v1.1 (1df371cc) and the Gemma paths-info call (W6)
- [ ] `decoder.path`/`sha256` = `scripts/lb/decode_hf_vlm.py` / e2de1881… (§3, §4)
- [ ] `venv.packages` = torch 2.5.1+cu121, torchvision 0.20.1+cu121, transformers 4.57.6, accelerate 1.15.0; `add_only` num2words 0.5.14 (§3)
- [ ] `decode.prompts`: the four hashes equal the §3 table
- [ ] `decode.max_new_tokens` = short 60, detailed 160, short_en 60, detailed_en 160 (§3, §4)
- [ ] `models` keys and order = §2.1 orders 1–6
- [ ] each `hub_id` @ `revision` = the §2.1 table
- [ ] `batch_size` = 1 for all six (§3)
- [ ] `dtype` is bf16 except llava15_7b, which is fp16 (§3); llava16 is bf16 per §2.1 row 6 (F16 checkpoint)
- [ ] `processor_kwargs` is {} and `attn_implementation` is sdpa for all (§3)
- [ ] file counts: Aya 13, Gemma 13 with no null, Idefics3 12, LLaVA-1.5 15, SmolVLM2 14, LLaVA-1.6 15 (§2.1 "Pins")
- [ ] copied blocks are diff-equal to their sources except `batch_size` and Gemma's 4 hashes (W6)
- [ ] `datasets.xm600`: manifest sha d414e04e…, 600 images, `image_dir` xm600; `datasets.xm600f50`: a455a816…, 50 images, `image_dir` xm600 (§4, §5)
- [ ] `runs`: `ae3_<key>_{xm600f50,xm600}-{short,detailed,short_en,detailed_en}`, 48 in all, equal to the job's `R=` patterns (§4, §5)
- [ ] `SHA256SUMS_E3` lists the §4 files plus v1 as a record, including job b11a9f6b; the job reads exactly this name (l.40)
