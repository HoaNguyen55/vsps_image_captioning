# PINS-A amendment to C-PVR-T1 — DRAFT

DRAFT, not committed, not judge-read. Written 2026-11-02T15:42:28Z (`date -u`). Internal prereg record, not paper text.

**What this is.** Prereg `PREREG_DRAFT_v1_2.md` (0a2f0773, commit 8282874) §9.1 step 5, PINS-A (one-judge read): it pins
the captioner and verifier (hub id @ revision), prompts, k = 4, greedy decoding, decomposers, the EN map (N13), the
proxy regex/extractor and `rapidfuzz` version, the retrieval encoder (NB-ENC), the OpenViVQA revision + 3 json shas +
image-file LFS shas (NB-OVQA, §8.1), `OI_TEST_URL` and the `c_pvr.py` sha (B3), the parity input shas (NB-PARITY) and
the M1 cap re-base rule (NB-CAP). It also carries CC-229 W2 and W3.

**Inputs** (sha256, first 8 hex):
- amendment `AMENDMENT_CC222_DRAFT_v1_3.md` c565e67a (commit db97b93);
- erratum CC-227 v3 `ERRATUM_CC227_GA_SCHEMA.md` a116fa85;
- `G_C1_record.json` 1f65b2ae and `G_C2_record.json` 767998f8 (commit 2ab08b3);
- `scripts/c_pvr/gates.py` bf4d5f64;
- `CC-229.txt` d5e1c604.

**Rules applied:**
- N7: models are picked by the fixed candidate order, never by Flickr counts or scores (CC-222 v1.3 l.579-580).
- Values come from the public HF API without auth or token. Repo revisions are commit hashes. A file sha is given only
  for a file already on disk, or as the hub's LFS sha256 from pointer metadata; no weight or data file was downloaded.
- **Nothing is guessed.** Every value that cannot be filled now is an explicit **OPEN** row with its reason.
- The companion pivot-checkpoint draft, `C_PIVOT_CHECKPOINT_DRAFT.md`, must reach CONTINUE before this amendment is
  read.

## 0. Status summary

| # | PINS-A item (prereg §9.1 l.632-635) | state |
|---|---|---|
| A1 | VI captioner, hub id @ revision | FILLED |
| A2 | VI verifier, hub id @ revision | FILLED |
| A3 | EN benchmark captioner / verifier | FILLED (vision-tower weight sha: see row) |
| A4 | prompts | **OPEN** |
| A5 | k = 4, greedy | FILLED |
| A6 | decomposers (VI, EN) | **OPEN** |
| A7 | EN map (N13) | **OPEN** |
| A8 | proxy regex / extractor / normaliser, `rapidfuzz` version | **OPEN** |
| A9 | retrieval encoder (NB-ENC) | FILLED |
| A10 | OpenViVQA revision, 3 json sha256, image LFS sha256 (NB-OVQA, §8.1) | revision + image LFS FILLED; **3 json sha256 OPEN** |
| A11 | `OI_TEST_URL` value; `c_pvr.py` sha (B3) | value FILLED; **`c_pvr.py` sha OPEN** |
| A12 | parity input shas (NB-PARITY) | FILLED (re-verified on disk) |
| A13 | M1 cap re-base rule (NB-CAP) | rule FILLED; **P1 OPEN** (speed test) |
| W2 | CC-229 OpenViVQA disclosure | carried verbatim |
| W3 | Flickr exclusion union for the pinned set; drop in n_e_power | union FILLED (4); **n_e_power drop OPEN** |

## 1. Model selection by N7 (A1, A2, A3)

**Fixed order** (`G_C1_record.json` `candidate_order`, closed 2026-11-02T00:27:14Z before any status):
1. Vintern-1B-v3_5
2. Vintern-1B-v2
3. Qwen2.5-VL-7B-Instruct
4. InternVL3-8B
5. aya-vision-8b
6. mblip-bloomz-7b
7. mblip-mt0-xl
8. Pangea-7B
9. centurio_aya
10. centurio_qwen

**Sets each role needs:**
- VI captioner: nocaps_test (P_obj^VI, R_obj^VI) and openvivqa_dev (proxy captions).
- VI verifier: v4.1 l.276, "the first model passing B10 for every registered test set", i.e. nocaps_test and
  openvivqa_dev.
- `vitextcaps_test` and `viecap4h_private_test` are conditional and DEFERRED (CC-222 v1.3 §5.4 l.556-557). Each needs its
  own amendment on release, and they do not block this pick.

| order | model | nocaps_test | openvivqa_dev | pick |
|---|---|---|---|---|
| 1-5 | Vintern-1B-v3_5, Vintern-1B-v2, Qwen2.5-VL-7B, InternVL3-8B, Aya-Vision-8B | UNCHECKABLE (G-C1) | UNCHECKABLE (G-C1) | skipped |
| **6** | **Gregor/mblip-bloomz-7b** | **CLEAN** (G-C2) | **CLEAN** (G-C2; CC-229 Q2, web-crawl branch) | **VI captioner and VI verifier** |
| 7 | Gregor/mblip-mt0-xl | CLEAN | CLEAN | not pinned (order 7 comes after a passing order 6) |
| 8 | neulab/Pangea-7B | UNCHECKABLE (G-C2, decided by documentation) | UNCHECKABLE | — |
| 9-10 | centurio_aya, centurio_qwen | UNCHECKABLE (G-C1) | UNCHECKABLE | — |
| EN | liuhaotian/llava-v1.5-7b | CLEAN (G-C2) | N/A | EN benchmark captioner and verifier (prereg l.457; v4.1 l.264) |

The VI pick is not a choice among options: order 6 is the first model CLEAN on both needed sets. Captioner and verifier
may be the same model (v4.1 l.264). No Vintern model is pinned, so the Vintern-only exclusion of prereg l.367 does
not fire, and O_B keeps its tier-2 role.

### A1 / A2 — VI captioner and VI verifier

| field | value | source |
|---|---|---|
| hub id | `Gregor/mblip-bloomz-7b` | G-C1 order 6; G-C2 CLEAN |
| revision | `4d95b91d56fcdce86504c951a28f016b15e219a1` | `https://huggingface.co/api/models/Gregor/mblip-bloomz-7b` field `sha`, read 2026-11-02T15:24:28Z (`lastModified` 2024-04-28T06:21:29Z); equals the G-C1 S12 card revision |
| gated / private | false / false | same response |
| `model-00001-of-00002.safetensors` | LFS sha256 `44be39143faaddf0b43e45f61f1d15a2804f0397e542e3c87b922a11b91a4c16`, 9,922,998,656 B | tree API at the revision, 15:24:35Z |
| `model-00002-of-00002.safetensors` | LFS sha256 `19dcdb305a64144c84cb9f924cf760e4577f7c4233d37048e63f89df5f9e95d6`, 8,592,229,664 B | same |
| `tokenizer.json` | LFS sha256 `17a208233d2ee8d8c83b23bc214df737c44806a1919f444e89b31e586cd956ba`, 14,500,471 B | same |
| `config.json` | git-blob SHA-1 `b56aa3dec29cdc24a1cb4537c65f7dbdac81b532` (not sha256; non-LFS); raw bytes at the revision: sha256 `39cac8ff4edd7c57f6514e105fede0d42d939ac7b40bf795a91646d23bc7b7a9` (fetched 15:42:20Z, 7,169 B) | tree API; raw `…/raw/4d95b91d…/config.json` |
| other non-LFS files | `preprocessor_config.json` 0b0fa393…, `model.safetensors.index.json` 9465df3c…, `special_tokens_map.json` fdafe480…, `tokenizer_config.json` 612d97d5… (git-blob SHA-1) | tree API |
| `.bin` shards (not to be loaded) | `pytorch_model-00001-of-00002.bin` LFS f5c563a6…, `-00002` LFS ee92b456… | tree API |
| loader | `transformers` `Blip2ForConditionalGeneration` / `Blip2Processor` (card S12, "For code examples, we refer to the BLIP-2 documentation"); safetensors only | card |
| web-scale pretraining | "unknown (disclosed)"; web component: Web CapFilt (CC3M + CC12M + SBU) | `G_C2_record.json` |
| Flickr host forms unparsed (PI risk control (1)) | `n_flickr_host_unparsed` = 0 in `mblip_capfilt_raw.scan.json` (128,759 static-host hits), 0 in both mixes | committed scan records (2ab08b3) |

**Load-time check (binding on `c_pvr.py`):** the GPU job downloads only at this revision. It asserts the sha256 of every
loaded safetensors shard and of `tokenizer.json` against this table, and the sha256 of `config.json` against
39cac8ff. Any mismatch is a FAULT and nothing is decoded.

### A3 — EN benchmark captioner and verifier (S1-S5)

| field | value | source |
|---|---|---|
| hub id | `liuhaotian/llava-v1.5-7b` | prereg l.457; G-C2 CLEAN on nocaps_test |
| revision | `4481d270cc22fd5c4d1bb5df129622006ccd9234` | API `sha`, 15:24:28Z (`lastModified` 2024-05-08); equals G-C1 S23 |
| `pytorch_model-00001-of-00002.bin` | LFS sha256 `492fdfa63cf314097d99da81a3586d54a97adc1471a0ae0535f5caa269b86314`, 9,976,634,558 B | tree API 15:24:35Z |
| `pytorch_model-00002-of-00002.bin` | LFS sha256 `c0eb94eb3fa578a4c63567f2eca6b0acf6a44a891c257aca0df88ffa891de72e`, 3,542,276,251 B | same |
| `mm_projector.bin` | LFS sha256 `be33a3b477e091832a3c8a9fabf5769c43b4cb2c161fc8c464b7bb214f16143a`, 41,961,085 B | same |
| `tokenizer.model` | LFS sha256 `9e556afd44213b6bd1be2b850ebbbd98f5481437a8021afaf58ee7fb1818d347`, 499,723 B | same |
| `config.json` | raw sha256 `f112de882e31171a105f0d3f69d9e6e8700a40149f0944f4b507d3a41789e492` (1,161 B; `mm_vision_tower` = `openai/clip-vit-large-patch14-336`, `transformers_version` 4.31.0) | raw at revision, 15:42:20Z |
| vision tower | `openai/clip-vit-large-patch14-336` @ `ce19dc912ca5cd21c8a653c79e251e808ccabcd1` (API `sha`, 15:42:28Z) | API; **weight LFS sha not fetched (OPEN-minor; fill at the same read or at load)** |
| inference code | the LLaVA GitHub code at a pinned commit (G-C1 cites c121f04 for the README only) | **OPEN-minor:** not a §9.1 item, but S1-S5 are not reproducible without it |
| flickr_matched_ids | none (`G_C2_record.json`) | — |

## 2. A4 — Prompts: **OPEN**

**Reason.** No C prompt file exists: `scripts/c_pvr/` holds only `gates.py`, `gates_mutants.py`, `SHA256SUMS` and the
idcheck files, and `rescap/vlm/` has no mBLIP adapter. A prompt is pinned by the sha of a file. Writing that file is
code work for the PINS-A round, and no prompt may be tried on any data before it is pinned. **No prompt was tested.**

These texts are needed, each in one file pinned by sha:
- P-cap-VI: zero-shot and k-shot caption prompts (A0, A1-A7, PVR); the same template for every arm, differing only in
  the demonstration block.
- P-ver-VI: the FAIR 3-label verifier prompt (SUPPORTED / UNCERTAIN / REJECTED; `rescap/metrics_svp.py` l.51) and its
  parser.
- P-corr-VI: the A8 post-hoc correction prompt, using the same verifier prompt and the same per-image verifier-call cap.
- P-A9, P-A10, P-A11 helper prompts, if those arms survive the §5.1 cut order.
- P-cap-EN, P-ver-EN, P-corr-EN for S1-S5 with LLaVA.

**Documented candidates [proposal], to be decided at the PINS-A read, not chosen here:**
- Caption: mBLIP's evaluation template "Caption in $LANGUAGE:" (S15 Table 8) with $LANGUAGE = Vietnamese. The
  instruction language follows mBLIP §3: English prompts that explicitly name the target language. Demonstrations are
  prepended as plain text.
- Verifier: **conflict found, for the reader.**
  - v4.1 l.276 says the verifier runs with "đúng prompt 3 nhãn của FAIR" (FAIR's exact 3-label prompt). Prereg §6.1
    says: label-generating prompt, label parsing, greedy, **no scalar threshold**.
  - `rescap/` was searched (`metrics_svp.py`, `svp/entailment.py`, `pipeline/`, `vlm/`) for a single prompt that
    generates SUPPORTED / UNCERTAIN / REJECTED. **None was found.**
  - FAIR's verifier is `rescap/pipeline/verify.py` (sha256 e1ce1682, last commit 07fd1d5). It builds the 3 labels from
    Vietnamese yes/no probes (`probe_yes_no`, `rescap/vlm/base.py` l.323, e8fee5bc; "Chỉ trả lời 'có' hoặc 'không'"),
    a stricter re-ask, a negation probe and C/S **thresholds** (`Thresholds`, verify.py l.20, l.295-315). It is not a
    label-generating prompt, and its thresholds conflict with §6.1.
  - So v4.1 l.276 **cannot be met as written**. The PINS-A read must either:
    1. name verify.py's probe procedure as "FAIR's 3-label scheme", with greedy decoding, `probe_k` = 1 and its
       thresholds pinned, and state that as an explicit override of §6.1; or
    2. register a new label-generating prompt and state that as an explicit override of v4.1 l.276.
  - Disclosed alternative under option 2 only: mBLIP's own 3-way template "Is it guaranteed true that "$HYPOTHESIS"?
    Yes, no, or maybe?" (S15 Table 8; neutral → "maybe"), mapped yes → SUPPORTED, maybe → UNCERTAIN, no → REJECTED,
    with parse failures → UNCERTAIN (prereg §6.3). Disclosed: mBLIP "fails to predict the neutral class" zero-shot
    (S15 §4.3).
  - In `base.py`, `k` means self-consistency samples at temperature ≥ 0.7. It is not C's k = 4 demonstrations.

## 3. A5 — k and decoding: FILLED

| item | value | source |
|---|---|---|
| demonstrations per prompt | **k = 4** (A1 top-k and every k-shot arm) | prereg §5.1 l.385, §0 l.148 |
| decoding | **greedy** (no sampling, beam 1), every arm and every model, VI and EN | prereg §5.1 l.385, §6.1 l.450-451 |
| `max_new_tokens` | **OPEN** (not registered; set in the prompt files of A4, before any output) | — |

The published mBLIP numbers use beam 5 (S15 §4.1), so they are not at C's decoding. This is disclosed, not changed.

## 4. A6 — Decomposers: **OPEN**

**Reason.** The prereg asks for deterministic rule-based decomposers: a VI segmenter, and an EN dependency parse (§6.2
l.458). Neither tool is pinned on the laptop now:
- `spacy` is not installed;
- the VnCoreNLP jar is not on the laptop (searched `~` and `data/` to depth 4);
- no C decomposer code exists.

**Candidates [proposal]:**
- VI: VnCoreNLP-1.2 RDRSegmenter (rule-based). The jar sha256 is `9e2811cdbc2ddfc71d04be5dc36e185c88dcd1ad4d5d69e4ff2e1369dccf7793` as pinned in the house B protocol (`scripts/b2_external/b2.py` l.1084). It must be re-hashed on the host that runs it.
- VI, alternative: `pyvi` 0.1.1, installed on the laptop (`importlib.metadata`). It is a trained CRF, not rule-based,
  so it needs the reader's acceptance.
- EN: a dependency parser with a pinned model package (e.g. spaCy `en_core_web_sm` at an exact version). **None is
  chosen here.**

The decomposer code (proposition rules, scene-text propositions included, per prereg §1.3) is new code with its own sha.

## 5. A7 — EN map (N13): **OPEN**

**Reason.** `scripts/c_pvr/en_oiv7_map.json` does not exist, and no English lexicon has been chosen (prereg §3.4 l.321-323).
- Fixed input, on disk: `data/datasets/xm3600/oiv7/oidv7-class-descriptions.csv` sha256 `84a4373a0efb7fd6d93fe19b0e7ceb6c1b855c233d13b9b78a9a33655c9fdce3` (re-verified at drafting; class names only, no label rows).
- Needed: the English lexicon (source and sha), the build script (sha) and the output map (sha), frozen before G-B and
  never amended after. P_obj^EN stays descriptive and is never a gate.

## 6. A8 — Proxy regex / extractor / normaliser and `rapidfuzz`: **OPEN**

**Reason.** None of the files exists, and `rapidfuzz` is not installed on the laptop (`importlib.metadata`: not found).
The version must be the one installed on the scoring host (the laptop, prereg §11 `score`), pinned as an exact version
plus wheel sha256 before the first tier-1 output (prereg §6.4 l.483-484). Registered values that stay fixed: SESOI_T =
2.0 points P_text, δ_RT = 2.0, w ∈ {1, 0} (prereg §6.4).

## 7. A9 — Retrieval encoder (NB-ENC): FILLED

| field | value | source |
|---|---|---|
| hub id | `google/siglip2-so400m-patch14-384` | prereg §6.2 l.459; `scripts/c_en/cen_pool.py` l.139 |
| revision | `e8e487298228002f3d8a82e0cd5c8ea9c567f57f` | `cen_pool.py` l.27 `SIGREV` (CC-113 W3); confirmed by `https://huggingface.co/api/models/google/siglip2-so400m-patch14-384/revision/e8e48729…` → 200, 15:24:28Z; it is also the current `main` |
| `model.safetensors` | LFS sha256 `9f4f4a49f908ef0c979bce8ff5a5c0e88882dc6c5dc4304387cbbd152558e2c2`, 4,544,143,072 B | tree API 15:24:35Z |
| `tokenizer.json` / `tokenizer.model` | LFS sha256 `cb9140fae3ac5122c972d37adf83e1248471a38147ad76f8215c8872c6fd8322` / `61a7b147390c64585d6c3543dd6fc636906c9af3865a5548f27f31aee1d4c8e2` | same |
| dtype | float16 | `cen_pool.py` l.139 meta |
| web-scale pretraining | "unknown" (disclosed) | prereg §6.2 l.460-461 |

## 8. A10 — OpenViVQA (NB-OVQA, prereg §4.3, §8.1)

| field | value | source / state |
|---|---|---|
| repo | `uitnlp/OpenViVQA-dataset` (dataset; gated false, private false) | API, 15:24:28Z |
| **revision** | `cc85c24c863afb05b5a52f68950f9ba6b69975cf` (`lastModified` 2023-12-13T14:37:50Z; `main` at read time; never `main` by name in code) | API field `sha` — FILLED |
| `dev-images.zip` | LFS sha256 `ff6a0e878bd0718425b3bf7e0455322111dc6e1ea2410cfd3eb7703216580f06`, 165,039,269 B | tree API 15:24:35Z — FILLED (§8.1: a downloaded archive with another sha256 = FAULT) |
| `test-images.zip` | LFS sha256 `e0ea3a805731376c31c517abd114f2dca6d52f193444e9eaa6cb2513f9d957bf`, 152,452,885 B | FILLED (recorded only; C never fetches it, since the OpenViVQA test answers are hidden) |
| `train-images.zip` | LFS sha256 `b01ba9365acf041042ee6a5f4c4acef98b7abfec2d673aa1b7b40bb8d5a40ba7`, 1,337,946,616 B | FILLED (O_B images, tier 2 only) |
| `vlsp2023_dev_data.json` | 762,438 B; git-blob SHA-1 `415ddd8b6fbb01f2c5d9b8fa0b2554fd9149992d` (**not sha256**) | **sha256 OPEN** |
| `vlsp2023_test_data.json` | 2,500,527 B; git-blob SHA-1 `0ae3f6982b42391a985d9b5fe454ab482aa5bb4d` | **sha256 OPEN** |
| `vlsp2023_train_data.json` | 6,596,293 B; git-blob SHA-1 `dae982c1463f49708c976d5de4dae453cd5eb266` | **sha256 OPEN** |

- **Why the 3 json sha256 values are OPEN.** The json files are stored as plain git files, not LFS, so the hub gives
  only a git-blob SHA-1, not a sha256.
- The sha256 needs the bytes. Downloading them belongs to `c_pvr.py ovqa-pin` under the §4.3 custody rule
  (`~/.vsps_sealed/c_pvr/ovqa/`, 0700, ACCESS_LOG; keys and lengths only), not to this draft. They were not
  downloaded.
- `ovqa-pin` must:
  1. fetch at revision cc85c24c;
  2. check each file's git-blob SHA-1 (sha1 of `blob <size>\0` + bytes) against this table, as a cross-check;
  3. record the three sha256 values in the PINS-A commit or a gatekeeper LOG line;
  4. assert dev = 1,070 images / 3,545 QA (C_TEST l.28) from keys and lengths only.
- **That `vlsp2023_dev_data.json` is OpenViVQA dev is something `ovqa-pin` must assert. It is not a fact yet.** Any
  mismatch is a FAULT, and the proxy is not run.

## 9. A11 — `OI_TEST_URL` and `c_pvr.py` (B3)

| field | value | state |
|---|---|---|
| `OI_TEST_URL` | `"https://open-images-dataset.s3.amazonaws.com/test/{file}"` | FILLED: `scripts/c_pvr/gates.py` l.66 (bf4d5f64), pinned by value there (CC-222 v1.3 §8 row l.695). It was observed 200 `image/jpeg` by HEAD (CC-222 v1.3 §7). |
| `c_pvr.py` sha256 | — | **OPEN:** the file does not exist. PINS-A asserts that `c_pvr.py` carries the same string byte for byte (CC-222 v1.3 l.695), and its sha is pinned when it is written and read. |

## 10. A12 — Parity inputs (NB-PARITY, prereg §3.3 l.313-318): FILLED

Re-hashed on disk by `sha256sum` at drafting (files not opened). All equal prereg §2.3.

```
779afb19a4c3c25f100f871e92bbe8e937d6fa7f20ea75c4d0f7a23953056e76  data/datasets/xm3600/oiv7/xm3600-train-annotations-human-imagelabels.csv
b7967190d6b05d6c97d38fe238046091905aabfe5bd268df4efe1c2a9a3db9d0  data/datasets/xm3600/oiv7/xm3600-val-annotations-human-imagelabels.csv
06567dd986bf571db62d69af5abec0973a37f2552b1e00c50147cf490f72c19a  data/datasets/xm3600/oiv7/xm3600-test-annotations-human-imagelabels.csv
84a4373a0efb7fd6d93fe19b0e7ceb6c1b855c233d13b9b78a9a33655c9fdce3  data/datasets/xm3600/oiv7/oidv7-class-descriptions.csv
75c22a0814037cee2bf328101aefdb3852a499c3e65fcdb1707e8fa2992f6c07  data/datasets/xm3600/oiv7/fetch.sh
e1af682181bcbbdfea6c76fb083e90481aa834efa1138efde869c1cc21e40de0  data/datasets/xm3600/oiv7/full-train.md5
5770ed7c94cb6ae9ebd5e8746a95382d6475d0887c87ad4c05afa664ec840d8a  data/datasets/xm3600/oiv7/full-val.md5
2eebd937f99edec5267abd697f1b839d9846fc4ba4fd070d833b048bbc9ace54  data/datasets/xm3600/oiv7/full-test.md5
263015f9dc46ebe2cea80055e04ed39baf80a356f4e027cd3756464279135bef  data/xm3600/manifest.json
27f2b1ca3f2bf47d43c8f00e8409472c8d571eb720d47b8107a1c77bd208d16a  data/xm3600/vi_oiv7_map.json
e47d249ac7290070f2387d3fa8b22dac77728265ad276f55aa6520f5cbc591a3  rescap/chair.py
fbc945f2247418275144ac75b893f7c51f8951b9ea42018680d433775dd79eb9  rescap/vi/lexicon.py
```

Parity targets stay as registered: 2,119 images, 4,453 present / 8,276 absent pairs (manifest l.14, l.16-17). Any
difference is a FAULT and G-B does not run.

## 11. A13 — Cap re-base rule (NB-CAP, prereg §10.1 l.722-731)

- **Rule (FILLED).** Q-cost = YES (PI-1102a, LOG l.1140): **cap = min(⌈1.25 × P1⌉, 37) GPU-h**, one re-base for M1.
  - P1 = projected tier-1 GPU-h on M1, from speed-test throughput only (≤ 1.0 GPU-h; outputs discarded, never scored,
    NB-SPEED). It is never taken from any output.
  - 37 = the money ceiling ≤ 350k VND at 9,282 VND/h (LOG l.1109).
  - If ⌈1.25 × P1⌉ exceeds the cap, arms are cut in the §5.1 order. If it still does not fit, the PI decides before any
    decode, and no set is shrunk.
  - A cap stop is final; one resume is allowed only for machine loss.
- **P1: OPEN.** It does not exist until the speed test runs. The speed test needs Q11 = YES and §9.1 step 8.
- **Flag for the reader, not decided here.** Q-custody is also YES (PI-1102a), so a single-tenant rented 4090 may hold
  C's pixels and decodes, named by its own amendment.
  - 37 GPU-h is an M1 money ceiling. On a 4090 at 17,499 VND/h (LOG l.1109), 350k VND is about 20 GPU-h [est.;
    350,000 / 17,499 = 20.0].
  - If the tier-1 host is not M1, that amendment must restate the cap in GPU-h for its host. This draft does not
    change NB-CAP.

## 12. CC-229 W2 — OpenViVQA disclosure (carried verbatim)

**Internal records only** (PINS-A, the G-C2/tier-1 report). This string contains overlap wording, so it never enters
paper text (PI-1101o). Verbatim from CC-229, REQUIRED FIXES W2:

> "openvivqa_dev: OpenViVQA images are a Google Images web scrape (arXiv 2305.04183 §3.2.1); web-crawl overlap unknown, disclosed"

Basis: CC-229 Q2, GO 93, reversible 90; Ruling 7. Sources (D-a) arXiv abs 2305.04183 da4a4487…, (D-b) PDF v1
729426e7…, (D-c) HF card 192f1e47…, kept in `.session_backup/2026-11-02/cc229_pages/`.

**Paper-facing disclosure sentence** (CC-222 v1.3 §5.4 l.561-562, verbatim; the only W2 text allowed in the paper):

> "CLEAN on the Vietnamese sets rests on the published training-data documentation and a name check of the released training lists; web-crawled components are unknown."

## 13. CC-229 W3 — Flickr exclusion for the pinned set (N7)

| field | value | source / state |
|---|---|---|
| pinned models | VI captioner = VI verifier = `Gregor/mblip-bloomz-7b`; EN captioner = EN verifier = `liuhaotian/llava-v1.5-7b` | §1 |
| Flickr-matched ids, bloomz-7b | `513d6796c322ced5`, `821f75f1f4061c79`, `bfdd3df591001b36`, `c32ddd2ae971e5b5` | `G_C2_record.json` |
| Flickr-matched ids, llava-v1.5-7b | none | same |
| **union applied (class (d), `CAPFILT_RULE = "image"`)** | **4 images** (the 4 ids above). They leave P_obj^VI, R_obj^VI and the proxy at every tier, count only. EvalAI CIDEr-EN keeps the full split. | CC-222 v1.3 §5.5 l.571-578; it equals the record's union, because mt0-xl matches the same 4 |
| **drop in n_e_power from (d)** | **OPEN, upper bound 4.** Only the matched ids that carry ≥ 1 verified label on a mapped class reduce n_e(G-B). That is known only after G-B, which this draft does not run. It is printed beside the W25-flagged and lost counts (prereg §5.6, §7.3 (d)). | — |

## 14. OPEN rows (list for the reader)

| row | why open | closed by |
|---|---|---|
| A4 prompts (P-cap/P-ver/P-corr, VI and EN; `max_new_tokens`) | no prompt file exists; no mBLIP adapter in `rescap/vlm/` | prompt files written and pinned by sha at the PINS-A read; no prompt is tried on data before the pin |
| A6 VI decomposer | VnCoreNLP jar not on the laptop; `pyvi` 0.1.1 is not rule-based | reader picks (jar 9e2811cd re-hashed on the run host, or `pyvi` 0.1.1 accepted) |
| A6 EN dependency parser | spaCy (or any parser) not installed; no model pinned | exact package + model version + wheel sha |
| A6 decomposer code | does not exist | file sha |
| A7 EN map `en_oiv7_map.json` + English lexicon + builder | none exists | three shas, frozen before G-B |
| A8 proxy regex list, extractor, normaliser | none exists | file shas before the first tier-1 output |
| A8 `rapidfuzz` version | not installed on the laptop | exact version + wheel sha on the scoring host |
| A10 3 OpenViVQA json sha256 | non-LFS, so the hub gives only a git-blob SHA-1; the download belongs to `ovqa-pin` custody | `c_pvr.py ovqa-pin` at revision cc85c24c (SHA-1 cross-check, 1,070 / 3,545 asserts) |
| A11 `c_pvr.py` sha256 | file does not exist | written, read, pinned; asserts `OI_TEST_URL` byte-equal to `gates.py` l.66 |
| A13 P1 | needs the speed test (after Q11 = YES) | speed-test LOG line |
| W3 n_e_power drop from (d) | needs G-B labels | G-B (`gb_counts.json`) |
| A3 minor: CLIP tower weight sha; LLaVA inference-code commit | not fetched; not a §9.1 item | same PINS-A read or the load-time check |
| A4 verifier form | v4.1 l.276 ("FAIR's exact 3-label prompt") vs prereg §6.1 ("no scalar threshold"): FAIR's verify.py is a probe pipeline with thresholds, and no single 3-label prompt exists in `rescap/` | explicit override of one of the two lines at the PINS-A read (§2) |
| A1/A3 minor: `transformers` / `torch` (and LLaVA code) versions on the GPU host | not installed on the laptop; greedy decodes are not reproducible without them | exact versions + wheel shas in the GPU job's lock file |

## 15. What this draft does not change

- No registered gate, threshold, status or rule changes. `gates.py` bf4d5f64, provenance e242623f, G-C1 1f65b2ae, G-C2
  767998f8 and SUMS are byte-unchanged.
- One look per test set.
- G-B still needs PINS-A and PINS-B committed and the Q11 ledger ruling at ≥ 92 (prereg §9.1 steps 5-7, §9.3).
- No LOG line. Not committed.

## 16. Network and file touches (`date -u`)

| when (UTC) | request | response sha256 (scratch copy) |
|---|---|---|
| 15:24:28Z window | GET `https://huggingface.co/api/models/Gregor/mblip-bloomz-7b` | 2f4c58de… (`…/c_pins/hf/models_Gregor_mblip-bloomz-7b.json`) |
| same | GET `…/api/models/Gregor/mblip-mt0-xl` | 9739ec17… |
| same | GET `…/api/models/liuhaotian/llava-v1.5-7b` | d3bfa800… |
| same | GET `…/api/models/google/siglip2-so400m-patch14-384` and `…/revision/e8e48729…` | 3c3e2335…, e45e65ac… |
| same | GET `…/api/datasets/uitnlp/OpenViVQA-dataset` | e153572e… |
| 15:24:35Z window | GET tree `?recursive=true` at each pinned revision (5 repos) | 8dd1fdde… (bloomz), 735cb471… (mt0), 8931c0e7… (llava), a3f5d9da… (siglip2), 6c2be14e… (OpenViVQA) |
| 15:42:20Z | GET raw `config.json` at the bloomz and llava revisions | 39cac8ff…, f112de88… |
| 15:42:28Z | GET `…/api/models/openai/clip-vit-large-patch14-336` | ebd7dfba… |

- Scratch folder: `/tmp/claude-1000/-mnt-d-vsps-image-captioning/078aa393-7328-44fb-9c0d-f6e088395441/scratchpad/c_pins/hf/`.
- Requests used curl with user-agent `vsps-research`. There was no auth, no HF token and no e-mail. No weight, image,
  zip or json data file was downloaded; the only raw files fetched were the two `config.json`.
- **The coordinator must copy these responses into `.session_backup/2026-11-02/` (named by sha256) before the
  one-judge read.**
- Local touches: `sha256sum` of the twelve files in §10 (not opened); `importlib.metadata` versions; `scripts/c_pvr/gates.py`
  l.66 by grep; `rescap/vlm/base.py` l.255-360 and `rescap/metrics.py` grep (code); the committed scan records'
  `n_flickr_*` fields; the mBLIP card copies S12/S13. No NoCaps, OpenViVQA, Objects365 or label file was opened.
