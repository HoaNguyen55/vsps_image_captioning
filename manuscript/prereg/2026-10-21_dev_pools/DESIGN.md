# Design note: dev-only zero-shot candidate pools (PD-31)

**Label: EXPLORATORY / DEV.**
- This note is not a registration. No registered claim may be made from these pools unless a prereg comes first.
- Every later prereg that uses them must list them under "what the author saw": which pools exist and what was computed on them.
- Model outputs are a method signal only, never gold or labels.

| field | value |
|---|---|
| Authority | PD-31 (`.session_backup/2026-10-13/decisions/PD-31.txt`, YES with bindings, 85%) |
| Purpose | raw material for future training-free method papers |
| Machine | M3 only (one RTX 3090 24 GB, the user rule) |
| Status | written 2026-10-21. It is committed through the gatekeeper before any pool decode. No pool output exists. |

## 1. Files

| file | sha256 | role |
|---|---|---|
| `scripts/dev_pools/generate.py` | `7ffb7344a138f0be13b2f797e685e62d20f924ac5c405c54586374c810d32b7d` | the generator: `--selftest` (CPU), `--list-runs`, `--check-inputs`, `--run-id` |
| `scripts/dev_pools/build_lists.py` | `650d94707d124a84c1b67f75e5c76a41561c54b8e1c2403efcad34f944319a61` | builds the two manifests and the exclusion list. It reads ids, file names and image hashes only. |
| `manuscript/prereg/2026-10-21_dev_pools/ktvic_dev299.tsv` | `a4ac7fdbd904f2205845705f5235b9748225a83a07854b58e59a755b85e4186e` | KTVIC dev images: id, file, image sha256 (299 rows) |
| `manuscript/prereg/2026-10-21_dev_pools/uitviic_val.tsv` | `338252e13c7cc8e51c579ea7f0a81f96919bb1aebe499ce90a8e7c370742e5a4` | UIT-ViIC val (optional): id, file, image sha256 (924 rows) |
| `manuscript/prereg/2026-10-21_dev_pools/exclusion.json` | `c52a96d18925b974878ae1a970c3f9133fb3482216676fd41871eeabb68cc77f` | the refused test-set ids and image sha256s, plus the sha256 of each source file |

- `generate.py` pins the manifests, the exclusion list, the B-N1 registration and the LB decoder by sha256 (`PINS`). It refuses to run if any of them differs.
- It reuses two committed pieces unchanged:
  - the LB decoder `scripts/lb/decode_hf_vlm.py` (sha256 `e2de1881…`, pinned by B-N1). Its parts used here are model loading, the per-file snapshot check, fixed batch slices, resume from the partial file, and the greedy call.
  - G2-B's `prompt_text`, which sha-checks the prompt against `scripts/evaluate.py` PROMPTS.
- The only new code is the N-sample pool call, the per-image seed, the dev manifests and the test-set refusal.

## 2. Models (registered snapshots, sha-pinned)

Both model blocks come from `manuscript/prereg/2026-10-19_b_n1_vi_leaderboard.json` (sha256 `9ff02dc2…`). That registration pins all 14 snapshot files of each model (LFS files by sha256, the rest by git blob sha1), and `lb.check_snapshot` verifies them before every run.

| key | hub id @ revision | licence | cross-check |
|---|---|---|---|
| `qwen25vl_7b` | `Qwen/Qwen2.5-VL-7B-Instruct` @ `cc594898137f460bfe9f0759e9844b3ce807cfb5` | Apache-2.0 | the 5 weight shards equal the B-F1 pins (`decode.base.shards_sha256`) |
| `qwen3vl_8b` | `Qwen/Qwen3-VL-8B-Instruct` @ `0c351dd01ed87e9c1b53cbc748cba10e6187ff3b` | **Apache-2.0**. The model card on M3 (`README.md` front matter `license: apache-2.0`, README sha256 `6d5d06e0…`) agrees with G2-B and B-N1. | the files equal G2-B's `SHA256SUMS` (`dc7bd4a4…`, 14/14 OK on M3) |

- **Shared settings:** bf16, sdpa attention, `AutoModelForImageTextToText`, `trust_remote_code=False`. Processor `min_pixels=262144`, `max_pixels=1048576`, left padding. These are B-N1's.
- **Venv:** B-N1's: torch 2.5.1+cu121, torchvision 0.20.1+cu121, transformers 4.57.6, accelerate 1.15.0, plus num2words 0.5.14.
  - On M3 this is a second venv, `/root/venv-lb`, separate from the B-F1 venv (transformers 4.51.3).
  - The generator refuses any other versions. The pip freeze sha256 is recorded per run.
  - The venv does not exist on M3 yet. Building it takes about 10 min and no GPU.

## 3. Prompts, caps, sampling, seed rule

- **Prompts:** `short` and `detailed`, verbatim from `scripts/evaluate.py` PROMPTS and sha-checked: short `8870589c…`, detailed `0addb5dd…`.
- **New-token caps:** short 60, detailed 160, the registered values of B-N1 and G2-B for both models.
- **Greedy:** `do_sample=False, num_beams=1`, in batches of 4. This is the LB decoder's call, so the greedy rows are directly comparable with the B-N1 harness.
- **Samples:** N = 8 per image at T ∈ {0.7, 1.0}, with `top_p=0.95, top_k=0`. These are the values of `scripts/e5_sample.py` and G2-B; `top_k=0` because Qwen's generation_config otherwise keeps sampling near-greedy.
  - Each call decodes one image with `num_return_sequences=8`. Every other setting comes from the snapshot's `generation_config.json`, which is recorded.
- **Seed rule:** before each image, `torch.manual_seed(int(sha256("42|model|mode|T|dataset|image_id")[:8], 16))`.
  - Each image's samples therefore depend only on (model, prompt, T, set, image). They do not depend on order, batching or a resume.
  - The seed is stored with each image.
- **Runs per set:** 2 models × 2 prompts × (1 greedy + 2 T × 8 samples). That is 12 runs and 68 captions per image (`--list-runs`).

## 4. Images

| set | images | source | notes |
|---|---|---|---|
| `ktvic_dev299` (primary) | 299 | KTVIC dev300 (`data/splits/ktvic_dev300.txt`, sha256 `cee024f8bb76846b1623e36d1861caccc4d13874db87544213a1f18f3de6898c`) | a fixed-seed sample of the KTVIC training images: B2's string-sorted `Random(0)` sample, md5 `e1af9069`, commit b44db13. One image is dropped (§5). |
| `uitviic_val` (optional) | 924 | all of UIT-ViIC val | run only if the budget is approved (§7) |

**dev300 is not fresh.** It was the dev set of the S1 gate and of other dev-side choices. Qwen3-VL zero-shot captions of dev300 already exist (the B1 step-1 outputs).

**UIT-ViIC val is not fresh either.**
- It was used for selection: the WiSE-FT gate chose α* on it.
- All 924 images are COCO train2014 (Karpathy split "train"), so exposure during pre-training is possible.
- Both facts must be disclosed wherever these pools are used.

Images are read from `$NCS_DATA/datasets/{ktvic,uitviic}/images` on M3, and each is checked against its manifest sha256 before decoding.

## 5. Exclusion list (PD-31 binding 3)

`exclusion.json` holds every image of a test set that either paper registered or used. `generate.py` refuses the whole run if any manifest row's id (in its namespace) or image sha256 is listed. The `--selftest` checks this with a KTVIC test id, a test-image sha and a COCO id.

| set | refused by |
|---|---|
| KTVIC test | 558 ids + 558 image sha256 |
| UIT-ViIC test (= uv231) | 231 COCO ids + 231 image sha256 (from the M3 copies) |
| CV295 | 295 COCO ids + 295 image sha256 |
| COCO-2500 | 2,500 COCO ids |
| COCO Karpathy test | 5,000 COCO ids (contains COCO-2500, all of CV295, 67 CHAIR-500 and 63 POPE images) |
| CHAIR-500 (COCO val2014) | 500 COCO ids + 500 image sha256 |
| POPE-500 (COCO val2014) | 500 COCO ids, from `data/results/pope_vi/zeroshot-vi.jsonl`, image field only |
| XM3600 (contains XM600) | 3,600 image sha256 (all local images) + the 600 XM600 ids |
| KTVIC dev near-duplicate of a test image | 1 id (`1437`) |

The COCO id union is 6,095 ids. The source files are hashed in `exclusion.json.sources`.

**Results:**
- **dev300:** 0 id hits.
  - 0 exact-sha hits against all 5,184 listed test-image hashes: KTVIC test, XM3600, CV295, CHAIR-500 and UIT-ViIC test.
  - One dev image (`1437`) and a KTVIC test image both match the same UIT-OpenViIC file under the registered match rule (`min(pHash, dHash) ≤ 10` and `SSCD ≥ 0.5`). That makes it a near-duplicate of a test image, so it is excluded, leaving 299 images.
  - Karpathy-test, COCO-2500 and POPE images are not on disk, so they are excluded by COCO id. KTVIC images come from a non-COCO pool, the UIT-EVJVQA images.
- **UIT-ViIC val:** 0 of 924 hit any listed set by id or sha. In particular, UIT-ViIC val ∩ COCO Karpathy test = 0, because all 924 images are Karpathy "train" (train2014).

**Recorded overlap, KTVIC dev300 ∩ UIT-OpenViIC (all splits).** The images stay in under PD-31, because we trained no zero-shot model on OpenViIC.
- 300/300 dev images match some OpenViIC file. The rule and its full-train counts reproduce the provenance exactly: 3,768, and 2,459 / 831 / 575 / 48.
- 296 of the 300 have a captioned copy.
- By the split of the copy: train 187, dev 57, test 59, uncaptioned 4. An image can match copies in more than one split.
- Only match records were read (`_pairs`), never an OpenViIC caption.

## 6. Output schema and provenance

- **Greedy runs** write `<run>.preds.json`: provenance plus `predictions {id: caption}`, `image_sha256`, `n_tokens` and `hit_max`.
- **Sampled runs** write `<run>.samples.jsonl`: one provenance line, then one line per image with `image_id`, `image_sha256`, `seed`, `samples [8]`, `n_tokens [8]` and `hit_max [8]`.
- Each output gets a `.sha256` sidecar.
- An existing output is never overwritten, and an interrupted run resumes from `<output>.partial.jsonl` (same run key only).
- **Provenance fields** (schema `vsps.dev_pools.v1`, enforced at write):
  - label `EXPLORATORY / DEV`, design path, run_id;
  - model, hub_id, revision, dataset, manifest and exclusion sha256;
  - prompt_mode and prompt sha256, max_new_tokens, temperature, sequences_per_image, generate_kwargs, seed_rule;
  - batch size, dtype, attention, processor kwargs, generation_config;
  - machine_id (M3's id), card, cuda;
  - git_head and git_dirty, job sha256, venv freeze sha256, generator sha256, inputs sha256 (PINS), packages;
  - n_images, resumed, started_utc and finished_utc.
- **Outputs:** `/root/outputs/dev_pools/` on M3, pulled by the 30-min backup loop.

## 7. Budget (RTX 3090, from logged speeds)

**Measured speeds:**

| decode | s/image | source |
|---|---|---|
| Greedy, batch 4, Qwen2.5-7B: short / detailed | 0.70 / 1.81 | B-N1, M1 3090, KTVIC test 558 |
| Greedy, batch 4, Qwen3-8B: short / detailed | 0.69 / 1.93 | B-N1, M1 3090, KTVIC test 558 |
| Batch-1 greedy, Qwen3: short / detailed | 1.37–1.73 / 10.3–10.9 | G2-B, M2 3090. Detailed always hits the 160 cap. |
| Batch-1 ×6 samples, Qwen3 short | 2.14 (1.56× its greedy) | G2-B UV231 |
| Batch-1 short greedy, Qwen2.5-7B + LoRA | 0.97 (558 in ~9 min) | B-F1, M3 |

**Estimated speed of the 8-sample pools (per image, per T):**
- short: 2.2–2.9 s
- detailed: 9–18 s. The low end assumes 8 sequences at the batched per-sequence rate; the high end assumes 1.7× the batch-1 detailed greedy.

**Per model and image:** 0.7 + 1.9 + 2 × (2.2–2.9 + 9–18) = 25–44 s. For two models that is 50–89 s per image.

| scope | captions | GPU-hours |
|---|---|---|
| **KTVIC dev299 only** | 20,332 | **4.4–7.6** (point estimate about 6), incl. about 0.2 h of model loads and slice-0 parity |
| UIT-ViIC val alone | 62,832 | 13.0–23.0 |
| **dev299 + UIT-ViIC val** | 83,164 | **17.4–30.6** |

**Order:**
1. Build `/root/venv-lb`.
2. Run `--check-inputs` for both models.
3. Run the 12 dev299 runs, greedy first.
4. UIT-ViIC val only after a separate go.

## 8. What this note does not do

- It registers no hypothesis, metric, threshold or verdict.
- It reads no reference and scores nothing.
- It never decodes a test-set image.
- Any later use of these pools needs its own prereg, with the pools listed under "what the author saw".
