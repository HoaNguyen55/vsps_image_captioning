# Paper B, B-2: description-only pre-registration of the kit run on external Vietnamese captioning systems

**Label: DESCRIPTIVE ONLY. No verdict, no ranking, no comparison with the group's registered numbers, no group system re-scored** (CC-126 W13). No B-2 decode, file content or score exists before this file and `scripts/b2_external/` are committed by the gatekeeper and judge-read.

| field | value |
|---|---|
| Paper | B (LRE; Q1 tier per PI-1026ah). One table "the kit on external systems" (§7) in §3.7 or the supplement. The sentence "validated on external systems" is allowed only under §7.3 |
| Bindings | CC-126 W13 (`.session_backup/2026-10-13/decisions/CC-126.txt` l.70); PI-1026af (B's own KTVIC test result is never re-scored); CC-130 (KTVIC train/test byte twins); UPGRADE_PLAN §7 (≥ 3 external systems) |
| Inventory input | `manuscript/ken/K15_ARTIFACTS_2026-10-27.md` §2.3, sha256 `a05a93751b027a65544fb9c5873f8ed08147287d1adee6dbf1b75d231b070d43`, identical to `.session_backup/2026-10-27/snapshots/SHA256SUMS` l.4 (checked 2026-10-27, INC-1027a) |
| Code | `scripts/b2_external/` (§11), `SHA256SUMS` there |
| Machines | laptop (fetch of class (a), structure gate, lists, all scoring, CPU); M3 (class-(b) fetch on CPU, then decodes on GPU) |
| Written | 2026-10-27 on the laptop, CPU only. No output file, checkpoint or prediction was downloaded; no caption was read (§10) |

## 0. Bindings

1. **Description only.** Every B-2 number is a descriptive row with its protocol columns. No row is called better, worse, competitive or state of the art; no row is placed beside, ranked with or differenced against any group system or registered number (P1, P1-R, fuse2, S4, S5 or any other). No group system and no group output is scored by B-2 (row 22 of the inventory and the 24 group systems of §3.4 are out).
2. **One split per system, the one it reports on** (§2). A system is never scored on a second test set.
3. **One look per system.** Each class-(b) system is decoded once and each system is scored once (`b2.py decode` refuses if its preds exist; `b2.py score` refuses if `scores.json` exists). A KTVIC-test row is logged in `scores.json :: looks` as that system's one look at KTVIC test. The group's KTVIC test result is not re-scored (PI-1026af).
4. **Caps:** ≤ 3 GPU-h (§6); CPU first (class (a) and all scoring are CPU; the GPU block only decodes).
5. **No caption** of any dataset or system is printed, quoted or committed. Fetched files, preds and the score folder stay under `.session_backup/2026-10-28/b2_external/` (laptop) and `/root/outputs/b2_external/` (M3, mirrored). Commits carry ids, counts, shas and aggregate scores only. UIT-OpenViIC enters only as aggregate scores (B §3.7).
6. **Isolation on M3:** B-2 holds `/root/outputs/b2_external/RUNNING` from `stage` to `cleanup`; it never runs beside C-2, B-1, G-RL or C-EN (§5.2). Staging lies under `/root/ncs-data/b2_stage` (CC-132 W1): inside `NCS_DATA`, so every `grl common.guard` (K2 Gate 0/0b, G-RL) refuses while B-2 test images are staged, and excluded from the 30-min backup; outside `NCS_DATA/datasets`, so `m3_clear` is unaffected.

## 1. Inventory, re-checked 2026-10-27 (metadata only)

Method: `huggingface.co/api/models/<id>?blobs=true` (revision, licence tag, files, sizes, LFS sha256), the model card's `README.md` grepped for dataset, split, metric and licence lines; `gh api repos/<r>` (licence, default branch, head) and `git/trees/<head>?recursive=1` (file names, sizes, blob sha1); README lines grepped. Classes: **(a)** published per-image test outputs; **(b)** a checkpoint runnable on one 24 GB GPU; **(c)** neither. Eligibility is separate: the system must report on a KTVIC, UIT-ViIC or UIT-OpenViIC test split (W13 sets; §0 item 2), be third-party and new, and pass the load rule of §2.3.

### 1.1 Ken's 22 rows (stable ids K1–K22)

| id | system | class | licence (scores) | reports on | B-2 |
|---|---|---|---|---|---|
| K1 | `Skyler215/Swin_BART_KTVIC` @`20044ae6…` | b (1.76 GB safetensors; decoder `vinai/bartpho-syllable`) | none (aggregates only) | KTVIC by model name only (card: "unknown dataset"; Bleu-4 0.2074 on an unnamed eval set; Q1 ruled: kept with this label) | **selected (b)**, KTVIC test |
| K2 | `SuperCoolGuy855/CLIP_mT5_Image_captioning` @`d786f6d7…` | a-candidate: `results.xlsx` (14,774 B; content unknown); no weights | none (aggregates only) | KTVIC test (README: "evaluated on the KTVIC test set each epoch"; data from the HF copy `Skyler215/KTVIC`) | **selected (a)**, subject to the gate |
| K3 | thesis-code baselines ResNet101+LSTM, ViT+Transformer | a | none; permission on file | KTVIC test | not new: scorer gate only (§3.2), not counted |
| K4 | `RinNguyen103/Vietnamese-Image-Captioning` | b only with a pickle (`.pth.tar`, 3.6 GB) and a custom class from an unlicensed repo | MIT | UIT-ViIC (card: "UIT-ViIC (train/val/test)") | **excluded by the load rule** (§2.3) |
| K5 | `thuanan/SmolVLM2-500M-vi-stage1` @`50467088…` | b (1.05 GB) | Apache-2.0 | UIT-ViIC test (card: ROUGE-L 21.94 on 200 samples, base 13.39) | **selected (b)**, UIT-ViIC test |
| K6 | `nviquang/Vie-BLIP` @`1ffe73cf…` | b (1.0 GB) | "other" (aggregates only) | UIT-OpenViIC (card: test split 2,001 images; "exact metric values are not included") | **selected (b)**, OpenViIC test |
| K7 | `nghiangh/OpenViIC` | c (code only, tree has no checkpoint or output) | none | OpenViIC | out |
| K8 | `pqthinh232/HCMUS-Qwen2-VL-2B-…-E1/E2/E3` + adapter | b | none | none (template card) | ineligible |
| K9 | `phatvo/MiniCPMV-2.6-Vietnamese-Caption` | b (16.2 GB) | none | none (card: document QA/OCR) | ineligible |
| K10 | `slyviee/vietnamese-image-captioning` | b | Apache-2.0 | none of the three (Flickr8k + MT COCO) | ineligible |
| K11 | `ttrung1402/blip2-…-adapters` (20 MB), `anhthuc5985/…-vit` (`.pth`) | b | none / Apache-2.0 | none | ineligible |
| K12 | VieCap4H solutions (`caodoanh2001/…`, `Luvata/…`) | c (expired links; medical domain) | none | VieCap4H | out |
| K13 | `QuangThai979/RobustCap` | c (no weights; tree: COCO files only) | none | none | out |
| K14 | `VuSnow/ViRA-VLM` | c (no weights) | none | none | out |
| K15 | Vintern-1B-v2 / v3.5 / 3B-beta | b | MIT / MIT / none | none (zero-shot only) | ineligible |
| K16 | LaVy (`chitb/LaVy-pretrain` 0.04 GB, `chitb/Lavy-instruct` PEFT adapter 0.67 GB) | b (adapter) | MIT / none | none | ineligible |
| K17 | `Vi-VLM/Vistral-V-7B` (gated: auto) | b (15 GB) | Apache-2.0 | none | ineligible |
| K18 | `VLAI-AIVN/llava-vietnamese-aio` | b (6.4 GB) | "other" | none | ineligible |
| K19 | mBLIP mt0-xl, bloomz-7b | b | MIT | XM3600 only (Paper A's, PD-24 c) | ineligible |
| K20 | `neulab/Pangea-7B` | b | Apache-2.0 | XM3600 only | ineligible |
| K21 | `WueNLP/centurio_qwen` | b | Apache-2.0 | XM3600 only | ineligible |
| K22 | Qwen2.5-VL / Qwen3-VL / InternVL3 S4 runs | group's own | — | — | out (§0 item 1) |

**Counts over K1–K22:** (a) 2 (K2 candidate, K3 not new); (b) 15 (K1, K4, K5, K6, K8–K11, K15–K21); (c) 4 (K7, K12–K14); group 1 (K22). Eligible and selected: K1, K5, K6 (b) and K2 (a).

### 1.2 Additions (cumulative ids X1–X9, W14)

Search on 2026-10-27, fixed now: `gh api search/repositories` for "KTVIC", "UIT-ViIC", "OpenViIC" and "vietnamese image captioning" (30 hits each), HF model search "ktvic" and "viic"; each Vietnamese-captioning hit's tree filtered for output-like file names (`pred|result|output|hyp|generated|submission` with `.json/.txt/.csv/.tsv/.xlsx`).

| id | source | file(s) at pinned commit (blob sha1, bytes) | class | licence | test set named | B-2 |
|---|---|---|---|---|---|---|
| X1 | `trannam710/NIC-with-Soft-Attention` @`06601183…` | `caption_results.json` (`a72cdf1a…`, 206,305) | a-candidate | MIT | UIT-ViIC (repo description) | **selected (a)** |
| X2 | `trannam710/Meshed-Memory-Transformer` @`61098012…` | `caption_results.json` (`b9273f0e…`, 114,497) | a-candidate | BSD-3-Clause | UIT-ViIC (repo description) | **selected (a)** |
| X3 | `vanngthi/ViECAP-Image-Captioning-Vietnamese` @`fd71ca59…` | `annotations/uit_viic_original_pred.json` (`3bbcd392…`, 117,525), `annotations/uit_viic_detect_pred.json` (`8b171c86…`, 121,967) | a-candidate; **one system, two variant rows** | none (aggregates only) | UIT-ViIC test (README: 231 images) | **selected (a)** |
| X4a–e | `loc110504/VietnameseSportImageCaptioning` @`6d8132e4…` | `notebooks/4_models/generated_captions/{cnn_lstm, cnn_lstm_attention, cnn_t5, qwen2, vit_t5}/uit_generated_captions.txt` (`6b786afb…`, `f50d655e…`, `aa132bf6…`, `671928f1…`, `34cd2779…`) | a-candidate; five systems, one source | MIT | "uit" by file name only; README describes an own sports dataset (Q9) | **selected (a)**, the gate decides |
| X5 | `tcm03/Vietnamese-image-captioning` | `baseline-2/result_vittrans.json`, blob `75f90f08…` = thesis-code's | duplicate of K3 | none | KTVIC | out (not new) |
| X6 | `AnhVu32/VietnameseImageCaptioning` | `ExpansionNet_v2/output_file.txt` | a? | none | none named | out |
| X7 | `Tin-Hoang/Image-Captioning-in-Vietnamese` | `RESULTS/Result_COCO5k_*.json` | a | none | COCO 5k (not a W13 set) | out |
| X8 | HF `tcm03/blip2_ktvic` | README only | c | Apache-2.0 | KTVIC | out |
| X9 | HF `ngwgsang/*-viic-*` (13 repos) | T5ForConditionalGeneration (text only) | c (no image model) | none | — | out |

**Totals:** class-(a) candidates selected: K2, X1, X2, X3, X4a–e = **9 systems from 4 sources** (K2 SuperCoolGuy855, X1–X2 trannam710, X3 vanngthi, X4 loc110504). Class (b) selected: K5, K1, K6 = **3 systems from 3 sources**. Upper bound 12 systems, 7 sources.

## 2. Selection, splits and decode recipes (fixed now)

### 2.1 Rule
All eligible class-(a) candidates first (CPU); then eligible class-(b) systems in the order K5 → K1 → K6 (first those with a reported score on the split, then by download size), each decoded once, until the cap binds (§6). Nothing in the rule depends on a B-2 score. The GPU block runs whatever the class-(a) gate gives (Q8), because K1 is the only possible new KTVIC-test row besides K2.

### 2.2 Splits
| system | set | images | references | KTVIC train |
|---|---|---|---|---|
| K2, K1 | KTVIC official test (`data/datasets/ktvic/test_data.json`) | 558 | 2,790 | yes (twins, §9) |
| X1–X4, K5 | UIT-ViIC official test (`uitviic/test_data.json`) | 231 | 1,155 | no |
| K6 | UIT-OpenViIC test (`openviic/uit-openviic-annotation-test.json`) | 2,001 | 10,001 | no |

### 2.3 Load rule and decode recipes (class (b), M3, `venv-lb` `685ffe2a…`: torch 2.5.1+cu121, transformers 4.57.6, huggingface_hub 0.36.2)
- **Load rule:** safetensors only, through `transformers` classes, `trust_remote_code=False`, `use_safetensors=True`; no pickle file is downloaded (`hf-fetch` takes only the pinned file names; `training_args.bin`, `*.bin`, `*.pth*`, `*.h5`, `optimizer.pt` never). Every file is checked against its pin (LFS sha256 for weights, git blob sha1 otherwise) at the pinned revision. Every model is loaded with `output_loading_info=True`: a non-empty `missing_keys` (after transformers' own ignore lists) is a load failure, so no weight is ever silently random-initialised; `unexpected_keys` are counted only and disclosed as a count in `smoke.json` and `prov.json` (CC-132 W3). **An error raised inside a registered `from_pretrained` / tokenizer constructor call, missing weights, or a failed registered artifact check (tokenizer class, vocabulary, special ids), makes that system class (c), reported as "not loadable under the registered recipe (transformers 4.57.6)", not as a fault of the third party** (`LOADFAIL` json, rc 4); no retry, no venv change, no other code. Any other error is treated as a bug of `b2.py` and is a JOB STOP (§8), so a recipe error is never recorded as the third party's failure. K4 needs a pickle and a custom class, so it is out by this rule.
- **Images:** `PIL.Image.open(...).convert("RGB")`, batch 1, `torch.manual_seed(0)`, each image's sha256 checked against the list before use.
- **K5 SmolVLM2** (`AutoProcessor`, `AutoModelForImageTextToText`, bf16; the processor's tokenizer must be the class declared in `tokenizer_config.json` or its Fast twin): the card's usage prompt (one user turn: image, then the text `Mô tả bức ảnh này.`), `apply_chat_template(add_generation_prompt=True)`, `generate(max_new_tokens=64, do_sample=False)`; only the generated tokens are decoded (the card decodes the prompt too).
- **K1 Swin-BART** (`VisionEncoderDecoderModel`, fp32; `ViTImageProcessor` from the checkpoint): `generate(pixel_values)` with the checkpoint's own `generation_config.json` (4 beams, max_length 29, no_repeat_ngram 3, length_penalty 2.0). Tokenizer, one path only: `PreTrainedTokenizerFast(tokenizer_file=tokenizer.json)` of `vinai/bartpho-syllable` @`36eee8b4…` (the decoder named in the checkpoint's config; `AutoTokenizer` is not used because the declared BartphoTokenizer needs sentencepiece, which venv-lb lacks, and anything else it built would be another class), accepted only if its size equals the decoder vocabulary (40,030) and `<s>`, `<pad>`, `</s>` are ids 0, 1, 2; otherwise LOADFAIL (Q5).
- **K6 Vie-BLIP** (`BlipImageProcessor` for the pixels, `AutoTokenizer` for decoding, which must build the declared `PhobertTokenizer`; `BlipForConditionalGeneration`, fp32; the card was written under transformers 5.0.0, venv-lb has 4.57.6, hence the explicit class check): the card's usage example, `generate(max_length=64, num_beams=5, early_stopping=True, no_repeat_ngram_size=3, repetition_penalty=1.5)` (the card's example, not the greedy `generation_config.json`; Q7).

## 3. Gates

### 3.1 Structure gate for class (a) (`b2.py gate`, laptop, once; counts only)
Fetched by `b2.py fetch`: only the pinned prediction files, from `raw.githubusercontent.com/<repo>/<commit>/<path>`, each checked against its git blob sha1; their sha256 recorded (`fetch.json`). Never a `*_gt.json`, a `test_data.json` or a dataset copy.
- **Parser (fixed):** JSON list of objects (or `{"annotations": [...]}`): id = first present of `image_id, id, img_id, image, file_name, filename, image_name, img`, caption = the one present of `caption, pred, prediction, predicted, generated, generated_caption, text, output, hypothesis` (a list → its first element); **a record or xlsx header with more than one of these keys is excluded as "ambiguous caption field"**, never resolved by key order (CC-132 W2a); JSON object: key → string, list (first) or object (caption keys); `.txt/.tsv/.csv`: one line per prediction, split at the first tab, comma or whitespace character, whichever comes first (ids contain none of them, so a comma inside a caption is kept); a first line whose id field is one of the id keys (case-insensitive) is one header line and is skipped; any other unknown id still fails (CC-132 W2b); `.xlsx`: first sheet, header row, the same key lists. Ids are normalised (basename, image extension dropped, leading zeros dropped) and mapped to the official test ids through the set's id and file-name aliases. **Never aligned by position.**
- **PASS iff** parseable; no unknown id; no duplicate id; the id set equals the official test id set exactly (558 / 231 / 2,001); the share of predictions equal to one of the same image's references (underscores to spaces, every punctuation character removed, lower-cased, whitespace collapsed; CC-132 W2c) is < 0.5 (a file that is a reference copy fails; Q10).
- **Any failure excludes the file with its reason; no repair.** A parser change is possible only by a dated amendment approved by the judge before `score` runs (no score of any system exists until then).
- `gate.json` holds counts only: rows, unknown, duplicates, covered, empty, refcopy share, file sha256, pass, reason.

### 3.2 Scorer gate (`b2.py score`, first step)
The kit re-scores the two published KTVIC baselines (K3; fetched 2026-10-22 at thesis-code `1a8d105`, blobs checked against `b2_controls.THESIS`; not counted, not new) and must reproduce `.session_backup/2026-10-22/b2/pilot_repro.json` (sha256 `f272d4b8…`) exactly at 2 dp: CIDEr-D under P0, syllable and pyvi, BLEU-4 and ROUGE-L under P0, for both. Else STOP. Run once on 2026-10-27 before commit to test the code: reproduced (§10 item 7). UIT-ViIC and OpenViIC have no external reproduction target; their gate is the image and reference counts of §2.2 (Q6).

## 4. Protocol columns (kit B; `protocol_pilot`, `ptb_protocol` imported unchanged)

Post-processing for every system, fixed: underscores replaced by spaces (count reported, B §3.4's rule for the released-segmented baselines), whitespace collapsed. References: the raw `caption` fields of the official test files.

| column | candidates and references | metrics |
|---|---|---|
| P0 | RDRSegmenter (VnCoreNLP 1.2, jar `9e2811cd…`), lower-cased, as written | CIDEr-D [95% CI], BLEU-4, ROUGE-L |
| P0s | P0, the candidate's final punctuation tokens stripped (`ptb_protocol.variants`), references as P0 | CIDEr-D |
| PTB | P0, then every token of pycocoevalcap's PTB punctuation list removed from candidates and references | CIDEr-D [95% CI], BLEU-4, ROUGE-L |
| SYL | syllables at whitespace, lower-cased (B §3.4 P1) | CIDEr-D |
| PYVI | pyvi word segmentation, lower-cased (B §3.4 P3) | CIDEr-D |
| counts | n; share ending in a punctuation token; PTB tokens removed and residual punctuation (`token_counts`); captions with underscores; empty captions | — |
| twins | KTVIC-trained systems only: P0 and PTB CIDEr-D, the per-image scores of the 558-image scorer (df over all 558 images' references) averaged over the 556 images without 1335 and 507 | CIDEr-D |

CIDEr-D df over the scored set's references; ×100. CI: percentile, B = 2,000, `numpy.random.default_rng(0).integers(0, n, (2000, n))`, images in sorted canonical-id order. Signature: `kitB|seg:rdr-1.2@9e2811cd|cider:D|scale:x100|punct:{as-written,final-stripped,ptb-removed}|refs:all`.

## 5. Procedure (frozen)

### 5.1 Laptop (CPU)
1. `b2.py fetch --out .session_backup/2026-10-28/b2_external/fetched` (blobs verified, `fetch.json`).
2. `b2.py gate --fetched … --data data/datasets --out …/gate.json` (once; counts only).
3. `b2_chain.sh <HEAD> dry-run` (lists: id, file, sha256 of the 558 KTVIC and 2,001 OpenViIC test images, id/file/url of the 231 UIT-ViIC test images; no caption; built once by `b2.py lists`, which refuses if any local image sha is in C-EN's test-side records). **The three lists are pinned (CC-132 W7):** `ktvic.tsv` `0a33004749ae47d0df8de22176d4fcc98e2be24b3bed664e18b65f18d9673ec2`, `openviic.tsv` `ce0f277f244df3cf692fc2f1ae5da2004fcb426537e735f999eeade6005b4858`, `uitviic.tsv` `4974b4c9c0e5d88bd2441fefc73662c853e8c1e9974aa43a730532902197ed4f`; the chain checks them in dry-run and stage before upload, and on M3 after upload; the dry-run says "lists pinned, overlap checked at build" (it does not re-check the overlap).

### 5.2 M3 (`b2_chain.sh stage | run | cleanup`, `b2_job.sh`)
- **stage** refuses on any tmux session, any `/root/outputs/*/RUNNING` or a failed `common.m3_clear`; takes `/root/outputs/b2_external/RUNNING` (noclobber) and holds it until cleanup; copies the KTVIC and OpenViIC test images by list to `/root/ncs-data/b2_stage/images/` (inside `NCS_DATA`, outside `NCS_DATA/datasets`; sha 558/558 and 2,001/2,001) and the lists. No reference file reaches M3.
- **job** (in tmux `b2`): HEAD, clean tree, both SHA256SUMS, venv-lb freeze; `b2.py guard` (M3, idle GPU, committed HEAD, `m3_clear`, inside tmux, no `cen*` session, no lock but B-2's own) before every GPU step; staged image shas re-checked, and none in `common.cen_test_shas()` (incl. nocaps_val); **CPU fetch** of the three pinned snapshots (+ the bartpho tokenizer) and of the 231 UIT-ViIC test images by `coco_url` (file-name rule, C-EN overlap refused), not charged to the cap; then a **smoke step per system before any test image** (GPU, charged): load by the recipe of §2.3, the tokenizer round trip on one author-written phrase (`chiếc ấm trà thạch anh tím đang hát ru bảy con sứa giấy bạc`, normalised equality) and one `generate` on a flat grey 384×384 image (non-empty string); it writes the tokenizer class, vocabulary size and caption length only; then **GPU decodes** K5 → K1 → K6 of the systems that passed, each under `timeout` (§6); `SHA256SUMS`; `BLOCK DONE`.
- **run** waits on `job.log` only, then mirrors and sha-confirms. **cleanup** mirrors, removes `/root/ncs-data/b2_stage` (test images and snapshots) and checks it is absent, re-runs `m3_clear`, releases the lock last.
- **Operator rule (CC-132 W8):** no C-EN step and no other M3 chain starts while `/root/outputs/b2_external/RUNNING` exists (`cen_fetch.no_pilot` does not check it; the B-1 and C-2 chains do).
- **Monitoring rule:** until `scores.json` exists no agent opens a preds file, a `dec_*` log or the fetched class-(a) files; monitoring reads `job.log`, `gpu_seconds.tsv`, return codes and counts.
- **Queue (CC-132 ruling 6):** C-EN NoCaps → K2 Gate 0/0b (+P1) → **B-2** → G-RL Gate 0 → P2 dev pilot. C-2 and B-1 are dev jobs on M4 (PI-1026ai); B-2 needs test images, so M3 only. If B-2 is committed and K2 cannot start, B-2 fills the gap (CC-126 W10). B-2 needs about 1–1.5 h of M3 wall time.

### 5.3 Score (laptop, once)
After BLOCK DONE or a final STOP: `b2.py score --data data/datasets --fetched … --gate …/gate.json --preds .session_backup/machines/M3/root/outputs/b2_external/preds --vnc .session_backup/machines/n2/ncs-data/vncorenlp --thesis .session_backup/2026-10-22/b2/thesis_code_1a8d105 --pilot .session_backup/2026-10-22/b2/pilot_repro.json --out .session_backup/2026-10-28/b2_external/score`. (jar `9e2811cd…`, checked by `score`). Writes `scores.json` (rows, looks, load failures, not-run systems, counts, scorer gate, code sha) and `table.md`, and prints one line that **the operator appends to `.session_backup/2026-10-13/decisions/LOG.md`**: `B2-LOOK | <utc> | systems scored: … | KTVIC-test one look of K1, K2 (those scored) | scores.json <sha256>` (CC-132 W6). `scores.json :: looks` stays. If M3 cannot run by 2026-11-30 (B's freeze), the judge may rule the GPU block final-not-run and `score` runs on class (a) alone.

## 6. Cap: 3 GPU-h (no GPU step starts after 2.5 GPU-h; a running step is killed at 3)

| item | basis | GPU-h |
|---|---|---|
| decodes, 231 + 558 + 2,001 = 2,790 images | reference rate, not a bound: Qwen2.5-VL-7B on M3, 0.69 s per image-arm (C test, `c_test/gpu_seconds.tsv`, C-EN PREREG l.134); K5, K1, K6 have about 0.5, 0.4 and 0.25 B parameters, but K1 and K6 use 4 and 5 beams at batch 1; not measured for these models | ≈ 0.53 |
| 3 smoke steps + 3 decode loads | not measured; budgeted at 5 min per load | 0.5 |
| **expected** | | **≈ 1.0** |

The bound is the cap (3 GPU-h, about 3× the estimate), not the rate.

Cap counting: `NAME start EPOCH` before and `NAME SECONDS` after each GPU step; an open start is charged to the next start or to now (reboot-safe). A timeout or the soft cap is a **CAP STOP, final**: no GPU step after it; the systems not decoded are reported as "not run (cap)". The fetches are CPU steps and not charged.

## 7. Report

### 7.1 Table (pre-written, `table.md`)
Title: "The kit on external systems (descriptive; no verdict, no ranking, not compared with the group's registered numbers)". Columns: id, system, source, test set, licence, then §4's columns. **Rows ordered by stable id, never by score. No rank column, no group row, no difference column, no bold.** Licence MIT, BSD-3-Clause or Apache-2.0: reported; none or "other": "aggregates only; permission not obtained" (Q3). Notes: each excluded file with its gate reason; each LOADFAIL as "not loadable under the registered recipe (transformers 4.57.6)"; the twins note (§9); each class-(b) system with neither preds nor LOADFAIL as "not run (cap)" if `CAP_STOP.json` exists, else "not run (JOB STOP)" (CC-132 W5).

### 7.2 Text allowed in B
- What the kit computes on each external system under each protocol column, and how the columns differ for that system (e.g. P0 vs PTB on UIT-ViIC, whose references end with periods). Statements about one system's own columns only.
- Not allowed: any comparison of an external row with a group number or with another external row's quality; "outperforms", "competitive", "SOTA"; any reading of the published scores of these systems as reproduced or refuted (their own protocols are unknown; a mismatch is stated as "protocol not matched").

### 7.3 "Validated on external systems"
`scores.json` reports `external_systems` (distinct ids; X3's two variants count once; X4a–e count five) and `distinct_sources` (repo owners). B may say "the kit was run on N external systems from M sources" for any N, and **"validated on external systems" only if N ≥ 3 AND M ≥ 3 distinct source owners** (`w13_validated_sentence_allowed`; CC-132 W4 / Q2, tightening W13 before any outcome). **Worst case:** every class-(a) file fails the gate and K1 fails the tokenizer rule → 2 systems (K5, K6) from 2 sources: **B cannot say "validated on external systems"** and the Q1 path of UPGRADE_PLAN §7 is not met by B-2.

## 8. STOP rules
- A pinned blob or LFS sha differs (fetch, hf-fetch) → STOP for that system to the judge (no substitute revision).
- Scorer gate fails → STOP before any external score.
- An image list, an image sha or a count (§2.2) differs → STOP.
- A staged image is in C-EN's test-side records → STOP (chain or job).
- Load failure (§2.3; incl. missing weights) → class (c) for that system, the job goes on; a smoke failure that is not a load failure (round trip, empty caption, any other error) → JOB STOP before any test image of that system, open to an amendment; any other decode failure → JOB STOP to the judge; a crash resumes with the same code (preds files are written atomically; existing ones are kept).
- Cap → CAP STOP, final (§6).
- After `scores.json`: no rescoring, no new system, no new column. A change goes into a dated amendment (§12) before the affected output exists.

## 9. Disclosures carried into every B-2 report
- **KTVIC byte twins (CC-130):** KTVIC train holds byte copies of two KTVIC test images: train 3589 = test 1335, train 7511 = test 507. K1 and K2 were (by name and README) trained on KTVIC train, K2 through the third-party HF copy `Skyler215/KTVIC` (no licence); their rows carry the twins note and the `_minus_twins` columns.
- **Test exposure:** K4's card lists UIT-ViIC "train/val/test" (excluded anyway); UIT-ViIC test images are COCO train2017 images (all 231 in Karpathy train), so COCO-pretrained backbones may have seen them (B §3.1); 555 of KTVIC's 558 test images appear in UIT-OpenViIC (B §3.1), so K6 may have seen KTVIC test images (it is scored on OpenViIC test only). OpenViIC test is Paper C's registered test set; a third-party decode there neither touches nor re-scores any C number.
- **Unknown protocols:** the published scores in the cards (K1 Bleu-4 0.2074 on an unnamed eval set, K5 ROUGE-L 21.94 on 200 samples) were produced under unknown protocols and are not compared.

## 10. What the author saw (and did not)
1. Ken's K15 §2.3 (sha verified) and §2.1; CC-126 W13–W17; Paper B `sec3_data_and_audit.md` §3.1, §3.3, §3.4, §3.7 and Table 3.1 (including the group's KTVIC numbers there, which B-2 never uses), `scripts/kit_b/PROTOCOL_CARD.md`; the kit code (`protocol_pilot`, `ptb_protocol`, `b2_controls`); the C-2 prereg, `c2_chain.sh` and `c2_job.sh` as templates; B-1 PREREG l.29/36 (twins); C-EN PREREG l.134 (rates); `scripts/grl/common.py`; the M3 venv-lb freeze (package versions).
2. **HF API metadata** of every HF row and search hit (revision, licence tag, files, sizes, LFS sha256) and the `config.json`, `generation_config.json` and `preprocessor_config.json` of K1, K6 and K5's generation config, and of `vinai/bartpho-syllable` (file list only).
3. **Model-card text:** K1's full card (a Trainer stub: Bleu-4 0.2074, eval set unnamed); K4 training table and usage code; K5 data mix, evaluation table and usage code; K6 dataset table, evaluation paragraph, licence paragraph and usage code (which includes one example output sentence written by the card author, not a dataset caption); keyword-grepped lines of the other cards.
4. **GitHub metadata:** repo records (licence, fork, description, head), full trees (names, sizes, blob shas) of the repos in §1, and README lines grepped for dataset, split, metric and licence words. The two thesis-code result blobs were compared by sha only for X5.
5. **Not opened or downloaded:** no class-(a) prediction file, no checkpoint, no `*_gt.json`, no dataset copy of any repo. No system output of any B-2 system has been seen.
6. **Local data, metadata only:** the structure (keys and counts) of the three test files; KTVIC test id ↔ file name (558 consistent); UIT-ViIC test ids against the Karpathy split (231 train, 0 val/test/restval); OpenViIC test 2,001 images / 10,001 captions; the three image lists (`.session_backup/2026-10-28/b2_external/lists/`, id, file, sha256 or url; no caption) were built with `b2.py lists` on 2026-10-27, with 0 overlap against the 10,000 C-EN test-side shas in the M3 mirror (coco_test, coco_kval; nocaps_val is checked on M3).
7. **Scorer gate, two runs before commit, pass/fail only:** the writer's (2026-10-27, laptop, `b2.scorer_gate`) and the judge's (CC-132 check 6, same jar `9e2811cd`); both reproduced pilot_repro.json (`f272d4b8…`) on the two thesis baselines, whose values have been known since 2026-10-22 (B §3.4). Ruled not a look (CC-132 ruling 3). **K1 vocabulary check (CC-132 check 5, metadata only):** `vinai/bartpho-syllable` @`36eee8b4` `tokenizer.json` is a Unigram vocabulary of 40,030 entries, ids 0/1/2 = `<s>`/`<pad>`/`</s>`, in the fairseq order `<s>, <pad>, </s>, <unk>` + `dict.txt` (40,029/40,029 match) then `<mask>`, so the single K1 tokenizer path decodes the ids the checkpoint was trained on (the smoke round trip cannot show this).

## 11. Code (`scripts/b2_external/`)

| file | role | where |
|---|---|---|
| `b2.py` | the pinned system list; fetch, gate, lists, hf-fetch, uit-fetch, guard, cap arithmetic, smoke, decode, score (re-gates the fetched files and requires equality with `gate.json`), table; `--selftest` (synthetic data only: parser and every gate reason, id aliases, the protocol columns with a stub segmenter, twins column, table without rank or caption, counts, cap and lock, the declared-class check and the LoadFail wrapper) | laptop / M3 |
| `b2_job.sh` | M3 job: preflight, CPU fetch, three smoke steps, then the decodes under the cap | M3 |
| `b2_chain.sh` | laptop chain: dry-run, stage (lock), run, cleanup (lock released last) | laptop |

Full shas in `scripts/b2_external/SHA256SUMS`; this folder's `SHA256SUMS` covers this file. Imported unchanged: `scripts/kit_b/protocol_pilot.py` (`rdr`, `Cider`, `bleu4`, `rouge_l`), `ptb_protocol.py` (`ptb`, `variants`, `token_counts`, `is_punct_tok`), `b2_controls.py` (`THESIS`), `scripts/grl/common.py` (`host_ok`, `m3_clear`, `cen_test_shas`, `fetch`). `b2.py --selftest` runs on the laptop only (it needs the kit's scipy, pyvi and openpyxl, which venv-lb does not pin); M3 runs the committed bytes (SHA256SUMS).

## 12. Amendments
None after commit. Before commit, CC-132 (GO-with-fixes) W1–W8 are applied in this file and the code: the staging path, the parser fixes, the loading-info rule, the ≥ 3 sources condition, the not-run notes, the LOG.md look line, the pinned lists and the text of §5.2, §5.3, §10 and §13. W9 (commit timing) is the gatekeeper's.

**Amendment 1 (2026-10-28, CC-138): smoke diagnostics, a second smoke input and the genuine-or-ours rule; no frozen value changes.**
- **STOP OPS-1028c-op.** The first M3 run at `1ae7339d` passed FETCH OK at 2026-10-27T21:02:11Z. Its first GPU step then stopped: `smoke_K5` gave JOB STOP rc=1 at 21:02:15Z, "K5 generated an empty string on the smoke image" (not a LOADFAIL). It used 4 GPU-s, which stay charged. No test image was decoded and no preds file exists. Cleanup ran at 21:04Z: `b2_stage` was removed, `m3_clear` passed and the lock was released. K1 and K6 were never smoked, because `stop()` ends the whole job.
- **Ruling CC-138.**
  - Q1: the class-(a) gate result is genuine. `gate.json` (`5519b26d`, 0/10 PASS) is final: no parser amendment and no re-gate.
  - Q4: the K5 empty output is not proven to be either ours or the model's. This amendment adds the means to tell the two apart before a restage.
  - §8 l.168 opens this smoke failure to an amendment. The outputs it affects (the K5/K1/K6 smoke and preds files, and `scores.json`) do not exist yet, so §8's last item is met.
- **W1, counts only.** For each input, `smoke` records n_new_tokens, n_special_new, first_new_is_eos and n_chars (the length of the decoded text). It writes them into `<sid>.smoke.json` or `<sid>.SMOKEFAIL.json` and prints them to the smoke log. The text itself is never written.
  - **New tokens:**
    - K5: `out[0, input_len:]`.
    - K1 and K6: the output with its first id dropped if that id is the decoder-start id or BLIP's injected bos id, then one more id dropped if it is a bos id (the tokenizer's, or K1's `forced_bos_token_id`).
  - **End ids (eos only):** the model's `generation_config.eos_token_id` and the tokenizer's eos id, plus, for K6, BLIP's text `sep_token_id` (the id BLIP's generate stops at). A pad id is not an end id: an immediate pad or `<|im_end|>` is case (b).
  - **Special ids:** `all_special_ids` plus the added tokens flagged special.
  - The decoded caption itself is unchanged, and so is every decode recipe of §2.3.
- **W2, second smoke input**, fixed by rule: the UIT-ViIC TRAIN image with the smallest integer id in `uitviic/train_data.json` whose sha256 is on no test-side list.
  - **Pinned:** id **368**, `000000000368.jpg` (COCO train2017, Karpathy train), sha256 **`58b0179921d415ca01b697255d473955e52559123e4a4b565e4d009dbb6c5f17`**.
  - **Selection:** the candidate was chosen by ids only, then fetched to the laptop by `coco_url` (`data/datasets/uitviic/images/`, git-ignored) and hashed. No caption was opened or printed.
  - **Laptop check, 0 hits on every list:**
    - KTVIC test (`ktvic.tsv`, 558);
    - OpenViIC test (`openviic.tsv`);
    - UIT-ViIC test (the mirrored `uitviic_test_images.sha256.tsv`, 231);
    - C-EN `coco_test`, `coco_kval` and `nocaps_val` (5,000, 5,000 and 4,500);
    - `exclusion.json` `image_sha256` (5,180);
    - `lists.json` `refuse.image_sha256` (all 6,599).
    The 22,260-sha union of these lists is a superset of the 21,336-sha test-side union of B-1/C-2 Amendment 2. Id 368 is also in no UIT-ViIC val/test list, no `exclusion.json` COCO id list and no Karpathy test/val list.
  - **On M3:** `b2.py smoke-fetch` fetches the image by `coco_url` (CPU, not charged) and refuses unless its sha equals the pin and lies outside `common.cen_test_shas()`. `smoke` re-checks the pin before use.
  - **Inputs:** the flat grey image stays the first input. The same two inputs apply to K5, K1 and K6.
- **W3, genuine-or-ours rule**, applied per input and then over both:
  - **(a)** new tokens that are not special and not end tokens, but decode to an empty (or whitespace-only) string: our decode bug, JOB STOP to the judge.
  - **(b)** a new token that is special but not an end token (e.g. `<image>`, `<|im_end|>`, a second bos): our template or processor, JOB STOP.
  - **Zero new tokens:** ours, JOB STOP.
  - (a), (b) and zero new tokens on either input override a pass on the other.
  - **(c)** only eos tokens on BOTH inputs (the first new token is eos): genuine. The result is `<sid>.SMOKEFAIL.json` with rc 5, and the table note "`<sid>`: not runnable: empty output under the registered recipe (transformers 4.57.6)" (§7.1 style, beside LOADFAIL). `scores.json` lists it under `smokefail`.
  - **(d)** text on either input: smoke PASS.
- **W4.** `b2_job.sh` continues on rc 5 as it does on rc 4. That system becomes class (c), and its smoke and decode are skipped on resume. Every other non-zero rc stays a JOB STOP. `b2.py --selftest` covers (a)–(d), zero new tokens, the precedence of a STOP over a pass, the BART-shaped prefix (`[2, 0, text, 2]` passes, `[2, 2]` gives (c)), the counts carrying no text, and the table note.
- **Disclosures.**
  - **(i) Post hoc diagnostic.** CC-138 check 4 was a structure-only read of the fetched class-(a) files (key names, value types, id shapes and id overlap counts; 0 non-ASCII characters, no caption value printed). It found:
    - K2: a per-epoch aggregate table;
    - X1/X2: no id field;
    - X3: 924/924 UIT-ViIC val ids;
    - X4a–e: 401 train / 149 val / 28 test ids.
    These are judge diagnostics, labelled post hoc, and not gate output.
  - **(ii) Deviation.** That read opened fetched class-(a) files before `scores.json` exists, against §5.2 l.133. It was caller-requested and structure-only. All 10 files are permanently excluded, so no score of them will ever exist. It is a disclosed deviation, not a look.
  - **(iii) Latent parser defect.** `CAP_KEYS` holds `caption` but not `caption pred`. Had X1/X2 carried an id field, the parser would have taken their reference column as the prediction, with only the reference-copy gate standing behind it. No file is affected (both fail on ids), so nothing is fixed.
- **Q1-path trigger (CC-138 W8).** If K5, K1 or K6 ends as LOADFAIL, SMOKEFAIL or not-run (cap, or a final JOB STOP), B-2 cannot give "validated on external systems". The coordinator then logs "B Q1 condition (UPGRADE_PLAN §7 l.106) not met by B-2; B targeted at LRE Q2 (l.128)" and tells the PI the same day. This amendment adds no system and no test set.
- **Unchanged:** the recipes, columns, splits, lists, cap, one look per system, the 0.5 reference-copy threshold and the ≥ 3 systems / ≥ 3 sources rule. The restage waits until the operator confirms on M3 that `/root/outputs/b2_external/RUNNING` is absent (CC-138 W7).
- **New code:** `b2.py` `a10ff192cb487142a209cd4e3e15e8dbcb244969a28391d2a12708ee66c5a549`, `b2_job.sh` `c78cd82901ed91e999f20ca8ded60d23dae2633fa554a3b516af4468c2c8990d`, `b2_chain.sh` unchanged (`714dc1f6…`). Full shas in `scripts/b2_external/SHA256SUMS`.

**Amendment 2 (2026-10-28, STOP OPS-1028f-op): truncated OpenViIC test files; no frozen value changes.**
- **Stop.** The restage at `2a7e12b8` passed smoke for K5, K1 and K6 (3 ok, 0 LOADFAIL, 0 SMOKEFAIL) and decoded K5 (UIT-ViIC) and K1 (KTVIC); `dec_K6` stopped after 32 s at 00:31:11Z with PIL `OSError: image file is truncated`. No K6 prediction was written or read; about 0.08 GPU-h were used in all.
- **Cause.** A CPU-only PIL decode of the 2,001 listed OpenViIC test images on the laptop (no caption read) finds exactly 3 files that fail strict decoding: `00000000768.jpg`, `00000001010.jpg`, `00000005095.jpg`. Their bytes match the pinned `openviic.tsv` shas, so they are truncated in the release itself. They are the same 3 files that Paper C's test rule already names (CC-082 T6, `scripts/c_test/ctest.py` `TRUNC`).
- **Rule (as C's T6).** Every image is decoded strictly first. Only these 3 named files, on a strict-decode failure, are opened once more with PIL `LOAD_TRUNCATED_IMAGES` set and reset around that one call; any other decode failure is a JOB STOP as before. The retried names are recorded in each system's `prov.json` (`truncated_retried`) and in the B-2 report notes, which name the 3 files as truncated in the release and decoded under T6. No image is excluded, so the full 2,001-image set is scored (full-datasets rule).
- **Code.** `b2.py` `52b8c145be0730f02f0ddd782c67dda26451063197ab19c6b723c54f5a783e6d` (`open_rgb`, `TRUNC`, selftest `_st_trunc`); `b2_job.sh` `finish()` (`88509ccb422ddd15f53dcf04e1a2e8c6387e196e3af5ee8a597cc1a92cb64076`) now leaves `logs/job.log` out of the output SHA256SUMS, because it appends "BLOCK DONE" to that file after hashing (the C-2 mirror-check STOP, CC-138c W1); `b2_chain.sh` unchanged. The K5 and K1 predictions already decoded under `2a7e12b8` are kept (one decode per system); their decode path read no OpenViIC image.

## 13. Questions, ruled in CC-132
1. **Q1** K1 is kept, labelled "KTVIC by model name only (card: unknown dataset)".
2. **Q2** "validated on external systems" needs ≥ 3 systems AND ≥ 3 distinct source owners, both reported (§7.3). K2 (SuperCoolGuy855) is a distinct source although it trained on Skyler215's data copy.
3. **Q3** aggregates only, "permission not obtained"; those predictions are never released; an optional courtesy email does not block.
4. **Q4** K4 excluded (pickle + unlicensed custom class).
5. **Q5** the single K1 tokenizer path is accepted (vocabulary order verified, §10 item 7).
6. **Q6** kit P0 on the raw `caption` fields; the count gate is the only gate on UIT-ViIC and OpenViIC.
7. **Q7** the author's documented usage example, else the checkpoint's `generation_config.json`; differences disclosed (K6: card 5 beams vs greedy config).
8. **Q8** the GPU block runs whatever class (a) gives.
9. **Q9** X4 kept; the gate decides.
10. **Q10** 0.5 kept, with the punctuation-robust comparison (§3.1).
11. **Q11** zero-shot VLMs out.
12. **Q12** slot as in §5.2 (ruling 6).
13. **Q13** `b2.py` is not split; the aislop 400-line warning is surfaced, not blocking.
14. **Q14** smoke step confirmed, charged to the cap, with the loading-info rule (§2.3).
