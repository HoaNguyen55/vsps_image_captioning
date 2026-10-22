# Paper E, stage 1: design note for dev-only exploration

**Label: EXPLORATORY / DEV.** This note is not a registration.

| field | value |
|---|---|
| Paper | E: a training-free, reference-free object-hallucination scorer for Vietnamese (and English) captions, checked object by object, with a count term |
| Authority | PI decision of 2026-10-22, 00:15 VN (`manuscript/cfp/QQ34_VENUES_AND_PLAN_2026-10-21.md`, §2.3, §2.4 and "Quyết định của PI") |
| Written | 2026-10-22, before any Paper E output exists. No judge probability, caption, embedding or metric of E exists. §10 lists what was read. |
| Machine | M3 only (one RTX 3090 24 GB), after Paper C's stage-1 run (§2.6). Every step that reads references or OIV7 labels runs locally on CPU, never on M3. |
| Code | `scripts/e_stage1/` (4 files). Their sha256 are in `SHA256SUMS` next to this note. `e_lists.py` pins this note's sha256, so this note cannot list the code's hashes. |

## 0. Bindings

1. **Outputs are never committed.** This covers pairs, caption files, model captions, judge caches, embeddings and the ledger. They live locally and on M3 under `/root/outputs/e_stage1/`, and in the 30-minute backup.
   - The only stage-1 file that may be committed is `e_split.json` (ids, file names, image sha256 and counts only), through the split addendum (§2.4).
2. **No registered claim comes from stage 1.** Every stage-1 number is a dev-A exploration number. It goes into the ledger and into the paper's "all configurations tried" appendix.
3. **Stage 2 needs its own prereg, committed before any E-dev-B image is judged or decoded.** It freezes the configuration picked in §7, the SESOI, the metrics and the kill rules (QQ34 §2.4: one look, CI lower bound > 0 and point estimate ≥ 2 × SESOI).
4. **A test prereg is committed before any XM-test2500 image is judged or decoded.** There is one test look.
5. **Order with Paper C (CC-081 E3, binding).** E's zero-shot decodes are C's `zs` arm (same backbones, prompt and pool), and E's per-object passes ask C's guard question. C's stage-2 and test runs in turn produce E's stage-2 and test data. So freshness is protected both ways:
   - **The order is fixed:** C stage 1 → C's stage-2 prereg committed → E stage 1 (≤ 4 GPU-h) → E's stage-2 prereg committed, or E stops → C's stage-2 run and E's stage-2 run. Any other order needs a judge round.
   - **Protecting C.** No E step on M3 touches a pair image (any XM-dev500 image) until C's stage-2 prereg is committed or C has stopped. C's stage-2 run must not take E's decodes or caches as its own outputs unless C's stage-2 prereg names that reuse.
   - **Protecting E.** E's stage-2 prereg (or E's stop) is committed before any C stage-2 output on XM-dev500 exists. E's test prereg is committed before any C test output on XM-test2500 exists, and E's test waits until C's test prereg is committed or C has stopped. If C runs first, the affected E look is reported as not fresh and goes back to the judge.
6. **No test-set tuning.** Stage 1 decodes and judges E-dev-A images only.
7. **No "first" or "novel" claims** ("đầu tiên" included), in any paper text. The paper states only differences from the closest work (QQ34 §2.3 table).
   - The image-minus-no-image (or null-image) contrast is not E's idea. The paper positions E against this prior work (source: `manuscript/ken/REVIEW_KEN_BATCH3_2026-10-22.md`):
     - token-level subtraction, used for decoding: C-PMI (NeurIPS 2025, 10.52202/085713-3516; arXiv 2505.19678) and VCD (arXiv 2311.16922, noised image);
     - token-level, used for scoring image–text matching with a null or noised image: MASS (AAAI 2025, 10.1609/aaai.v39i3.32262; arXiv 2501.11469, black null image) and VisualGPTScore (arXiv 2306.01879);
     - yes/no logit with a null image, at attribute level, used for VQA decisions: VISOR (arXiv 2608.11024), the closest;
     - object-level P(yes) without subtraction, used for hallucination detection: CapMAS "Isolation" (arXiv 2412.15484);
     - object-level confidence without subtraction, used for selection: Self-Validation (arXiv 2601.22451). Its LPFV is a single-word answer prompt p(o | v, x_e) with no subtraction; its JS divergence between with and without the image is a diagnostic only. The paper must not credit it with the subtraction.
   - FLEUR (ACL 2024, 10.18653/v1/2024.acl-long.205) and HalDec-Bench (arXiv 2511.20515) are context or baselines. FaithScore, ALOHa, HICEScore and MSD-Score are the closest metrics (QQ34 §2.3).
   - E's distinct point is object-level yes/no with a no-image subtraction, used as a reference-free caption metric with count calibration, evaluated in Vietnamese and English.
8. **Existing data and labels only.** No new annotation.
   - Gold is the XM3600 references and the Open Images V7 human-verified image labels, as released.
   - Judge probabilities, model captions and embeddings are model signals. They are never gold, labels or evidence.
9. **One GPU.** Everything runs on M3. No second machine is planned.
10. **No dataset caption is written into any committed file.**
   - Pair and caption files hold E-dev-A reference texts and are never committed.
   - Committed code holds only synthetic self-test strings made of placeholder syllables and object words.
11. **E measures controlled sensitivity, not agreement with people.** There is no Vietnamese human judgement of hallucination, and none is collected. The paper says so (QQ34 §2.3).
12. **E is never the main metric of Paper C or D** (QQ34 §2.3), so no paper confirms itself. E's per-object statistic is the same statistic as C's guard (§4.1); the paper states this.

## 1. Question and scorer

**Question (exploratory).** Does a training-free scorer rank captions by object hallucination better than global scorers, in Vietnamese as well as English? The scorer checks each mentioned object with a VLM, with and without the image. The global scorers are SigLIP2 or multilingual CLIP similarity, and a VLM asked about the whole caption. "Better" means two things, each at an equal object count:
- separating a caption that gains one fabricated object from one that gains one real object;
- following the OIV7-verified precision of real model captions.

**Scorer.** For a caption c of image i, with distinct mentioned classes M(c):
- `d(i, o) = P(yes | image i, question about o) − P(yes | no image, question about o)`;
- `E(c) = mean over o ∈ M(c) of d(i, o) − λ · max(0, |M(c)| − n̂)`.

Details:
- **Mentions** come from the rescap matcher v2 (`rescap.chair.objects_in`, through `guard.classes`). The English matcher is in §3.5. Classes are counted once per canonical key (`guard.key`).
- **Weights** are uniform over the distinct classes. This is fixed now and not explored.
- **The question about o does not contain the caption.** So d(i, o) depends on the image and the class only: one judge cache per (judge, question language) serves every caption.
- **The count term** comes from Paper A's count-matched finding: a metric can reward a caption for naming more objects. It penalises mentions beyond n̂.
  - n̂ is the median number of distinct mentions among the E-dev-A base references of the same language that name at least one class (§5).
  - λ is picked on dev-A by the fixed rule of §7.2. If no λ > 0 passes, λ = 0, and the paper drops the calibration claim, as QQ34 §2.3 allows.
- **Pooling over judges.** E is the mean over the judges, never including the judge that generated the caption (§5).
- A caption with no mention gets no score. In a pair it counts as a tie (§7.1).

## 2. Data

### 2.1 Sets

| set | images | definition | stage-1 use |
|---|---|---|---|
| XM600 | 600 | `$NCS_DATA/datasets/xm3600/test_data.json` (`data/xm3600_subset.txt`), Paper A's test set | refused |
| XM-dev500 | 500 | Paper C DESIGN §2.3: XM3600 minus XM600, ordered by sha256(`"paperC|xm|"` + image sha256), first 500. Computed with C's own `build_memory.split(rows, "xm", 500)`. | split below |
| **E-dev-A** | 250 | XM-dev500 ordered by sha256(`"paperE|xmdev|"` + image sha256), ties broken by id; the first 250 | **the only stage-1 set** |
| E-dev-B | 250 | the remaining 250 of XM-dev500 | refused; stage 2, one look |
| XM-test2500 | 2,500 | the rest of XM3600 minus XM600 | refused; E's (and C's) test |

- Only E-dev-A images that carry at least one verified label on a mapped class (§2.2) and at least one reference with a mention form pairs, and only they are decoded and judged. A local dry run (§10) found 128 labelled images, 121 of them with pairs. The authoritative counts come from `e_split.json` and `pairs.counts.json`.
- **Explicit carve-out.** Paper C's `exclusion.json` (sha256 `c52a96d1…`) refuses all 3,600 XM3600 images by sha256. E's stage 1 carves out **only the 250 E-dev-A sha256**.
  - `e_lists.refusal` checks that the carve-out lies inside `xm3600_all_images` and outside every other excluded set.
  - XM600 ids, E-dev-B, XM-test2500 and every other registered test image (KTVIC test, CV295, CHAIR-500, UIT-ViIC test) stay refused.
- `e_lists.py split --c-lists` cross-checks XM-dev500 against Paper C's `lists.json` once C has built it. The split refuses to write if the two sets differ.

### 2.2 Labels and the vocabulary map (Paper A's tooling, unchanged)

| file | sha256 | role |
|---|---|---|
| `data/xm3600/oiv7_labels.json` | `bac3953a…` | OIV7 human-verified image labels of the 3,600 XM3600 images (Confidence 1 = verified present, 0 = verified absent), CC BY 4.0 |
| `data/xm3600/vi_oiv7_map.json` | `27f2b1ca…` | lexicon class → OIV7 classes (`pos` and `neg`); 69 mapped classes |
| `scripts/xm3600_oiv7.py` | `9a79403f…` | `resolve_map` (display names to MIDs) and `statuses`: present if a `pos` class is verified positive, else absent if a `neg` class is verified negative, else unknown |
| `data/coco_probe/coco80_vi.json` | `926e0857…` | Vietnamese terms for the COCO-80 classes; source of the out-of-lexicon terms (§3.3) |

- **Verified precision** of a caption is present / (present + absent) over its distinct mentioned classes with a status. This is Paper A's `caption_rows` rule.
- Only captions with at least one verifiable mention enter τ.

### 2.3 Paper A's 150-image XM3600 adjacency set lies mostly outside XM600

- Paper C's judge asked that this set be confirmed to lie inside XM600. **It does not.**
  - The set is the XM3600 images with three Vietnamese references: 150 images. Paper A's N2 check used all 150 (`manuscript/prereg/2026-10-14_xm3600_predictions.json`, `observed_full_150_images`). Only 27 of them are in XM600.
  - The remaining 123 split as 7 in E-dev-A, 8 in E-dev-B and 108 in XM-test2500 (dry run, §10). `e_split.json` records these counts.
- **What was read.** N2 read the positions of shared objects across the three references of each image. It read no OIV7 label and no model output, and it was done on 2026-10-14.
- **Also already read over all 3,600 images.** These are aggregate OIV7 counts only, in `data/xm3600/manifest.json` `coverage`: classes mapped, images with labels, and present and absent pairs per class.
- **Rule (fixed by CC-081 E2):**
  - the 123 images stay in every set, and every primary analysis includes them; the paper discloses this;
  - both E's and C's test preregs add a sensitivity analysis without the 108 XM-test2500 images. It is reported next to the primary and never replaces it.

### 2.4 Split addendum (before any GPU step)

1. Run `e_lists.py split --c-lists <Paper C's committed lists.json>` locally (CPU). `--c-lists` is required (CC-081 E4).
   - It reads image bytes, ids, file names and per-image caption counts, and no caption.
   - It refuses unless XM-dev500 equals C's, and unless the counts reproduce 600 / 250 / 250 / 2,500 (XM600, E-dev-A, E-dev-B, XM-test2500) and 27 / 7 / 8 / 108 (Paper A's three-reference images in each). A mismatch goes back to the judge.
   - It runs its own n-gram scan and refuses to write if the scan finds a hit.
2. Commit `e_split.json`, the one-line change that sets `e_lists.SPLIT_SHA256`, and `SHA256SUMS` together, through the gatekeeper, who runs the 6/8-gram scan on them.
3. Every GPU step, and `pairs.py`, refuses while `SPLIT_SHA256` is unset (self-tested).

### 2.5 Refusal (enforced in code)

`e_lists.check_images` runs in every mode that reads or writes per-image data: `pairs.py build` and `items`, every `judge.py` mode, and `score.py`. It refuses any image that is not an E-dev-A image, or whose id or sha256 is refused (§2.1). The self-tests of `e_lists.py` and `judge.py` check the refusal with an XM600 id, an E-dev-B image, a non-XM3600 test image and an unknown id.

### 2.6 What goes to M3, and when

- **Preconditions.** E's GPU work on a pair image starts only when all four hold:
  - Paper C's stage-1 run has ended;
  - **either** C's stage-2 prereg is committed **or** C has stopped (binding 5; C's binding 3 forbids decoding XM-dev500 before C's stage-2 prereg);
  - the split addendum is committed;
  - the operator has removed E's test gold and the XM3600 annotations from M3 (below).
- **Allowed before that (XM-free).** Locally on CPU: the split addendum (once C's `lists.json` is committed) and `pairs.py build`, which prints counts only. On M3, touching no image: `lb.check_snapshot` and the fetch of a missing snapshot at its pinned revision, S2's shard check, whether open_clip and the M-CLIP weights are present (and in which venv), and a tokenizer-only check that có/Có/không/Không have distinct first tokens for both HF judges.
- **Copied to M3:**
  - the E-dev-A images that form pairs (about 121 files), into a folder holding nothing else. The run record keeps their count and sha256 list. Every `judge.py` mode refuses if the folder holds any file that is not an E-dev-A image;
  - `captions.jsonl` (E-dev-A reference and perturbed texts) and, after the decodes, `items.jsonl` and `captions_all.jsonl`. These hold E-dev-A references only, are never committed, and are never printed to logs.
- **Never copied:**
  - E-dev-B images (until the stage-2 prereg);
  - XM-test2500 and XM600 images;
  - the XM3600 annotation files (`full_data.json`, `test_data.json`, captions.zip).
- **Already on M3.** XM3600 images were removed from M3 on 2026-10-21 22:31Z for Paper C's stage 1. The operator checks that none is back before copying, and records the copy (file count and sha256 list) in the run record.
- **E's test gold is removed from M3 (CC-081 E1).** `data/xm3600/oiv7_labels.json` holds the XM-test2500 labels and is tracked in git, so a checkout puts it on M3.
  - Before E's first M3 step, the operator removes it from M3's working tree (`git update-index --skip-worktree` on the path, then delete) and records its absence in the run record. The record also notes that `$NCS_DATA/datasets/xm3600/` (including `oiv7/` and `raw/`) and `xm3600_en/` hold no annotation file, only the copied pair-image folder if it is placed there.
  - Every `judge.py` mode refuses while the labels file, an XM3600 or XM3600-en `full_data.json` / `test_data.json`, or the `oiv7/` or `raw/` folder is present on the host (`e_lists.m3_clean`, self-tested).
  - GPU modes hash only DESIGN, guard.py and clip_score.py (`e_lists.GPU_PINS`); a self-test asserts that this check never opens the labels or tooling files. The local modes (`split`, `pairs.py build` and `items`, `score.py`) also pin `xm3600_oiv7.py`, the labels, the map and `coco80_vi.json` (`LOCAL_PINS`), and refuse when `VSPS_MACHINE_ID` is set (the M3 job environment sets it).

## 3. Minimal pairs (`pairs.py build`, deterministic, no new annotation)

### 3.1 Base captions

- **Base captions** are the first two XM3600 references of each labelled E-dev-A image, in annotation order: Vietnamese (`xm3600/full_data.json`) and English (`xm3600_en/full_data.json`), as released, with whitespace collapsed.
- **Model captions** enter only the τ analysis (§3.6), never pairs.
- A base must name at least one class. A pair is kept only if the matcher finds exactly the expected class set in the perturbed caption (keys compared). Otherwise it is skipped and counted, per type.

### 3.2 Perturbation types and the correct winner

Notation: P are classes verified present on the image, A classes verified absent. "Free" means not mentioned in the base and not an ancestor or descendant (`rescap.chair._ancestors`) of a mention.

| type | languages | construction | correct ranking |
|---|---|---|---|
| `swap` | vi, en | a mentioned present class → a free absent class (its surface, §3.4) | base > perturbed |
| `add_absent` | vi, en | append one free absent class | base > perturbed |
| `add_present` | vi, en | append one free present class | none: Δ reported only |
| **bc** (count-matched) | vi, en | `add_present` vs `add_absent` on the same base: both gain one object | add_present > add_absent |
| `delete` | vi | drop the unit of a mentioned present class with C's `guard.delete`; skipped on its fallback | none: omission control, Δ reported only |
| `ool_absent` | vi | append a verified-absent object in a surface form the matcher misses (§3.3) | base > perturbed. E ties by construction: a test of the extractor, reported as E's limit |
| `pad` (count-mismatched) | vi, en | append a free present class and then a free absent class, unrelated to each other | base > perturbed (the count term is tested here) |
| `pad_control` | vi, en | append two free present classes, unrelated to each other | none: the share ranking the perturbed caption lower is a false alarm of the count term |

**Choice.** Each choice uses `random.Random(int(sha256("paperE|pair|<lang>|<image>|<ref>|<type>")[:8], 16))` on sorted candidates. Each (base, type) gives at most one pair.

### 3.3 Out-of-lexicon terms

- These are `coco80_vi.json` terms for which `objects_in` finds no class (89 terms with an exact OIV7 display-name match).
- A COCO class name must equal exactly one OIV7 display name, ignoring case. A term is absent on an image when that MID is verified negative and not positive.
- The map is tooling, as `coco80_vi.json` is: it creates no label.
- Construction: `và một <term>` is appended.

### 3.4 Vietnamese surfaces

- **Appended phrase.** The joiner is ` và `, then `một`, then the class with its classifier from `rescap.vi.lexicon.NOUN_CLASSIFIER`. The classifier is omitted when the class word starts with it.
- **Swap.** The base must contain the mentioned class's surface (classifier + class) exactly once as a whole word, ignoring case. That surface is replaced by the absent class's surface.
- The end punctuation (`guard.END`) is kept.

### 3.5 English (secondary; never gates)

- **Matcher.** rescap has no English matcher for the 112 classes. Stage 1 uses the head noun of S2's English noun phrase (`english_class_map`, e.g. "a dog" → "dog") for the 69 mapped classes.
  - It matches whole words, ignoring case, with regular plurals and four irregular ones (men, women, children, people), longest match first.
  - Heads shared by two class keys are dropped.
  - It has no synonyms. Its recall on English references is low: 93 of the English bases named no class in the dry run.
- **Appended phrase.** The joiner is ` and `, then S2's noun phrase. Swap replaces the head noun; the article is not adjusted.
- English has no `delete` and no `ool_absent`.

### 3.6 Real captions for τ

- **Models.** The four B-N1 generators decode the pair images of E-dev-A zero-shot: Qwen2.5-VL-3B @ `66285546…`, Qwen2.5-VL-7B @ `cc594898…`, Qwen3-VL-8B @ `0c351dd0…` and InternVL3-8B-hf @ `259a3b64…`.
- **Decoding.** The B-N1 `short` prompt (sha256 `8870589c…`), 60 new tokens, greedy, B-N1 batch sizes and venv. It goes through the committed LB decoder (`decode_hf_vlm.py`, pinned through C's `decode_icl.PINS`), wrapped as `decode_icl` wraps it.
- **Overlap with C.** These are the same backbones and prompt as Paper C's `zs` arm, on C's future dev-B pool. Disclosed; judge Q4.
- The decodes are copied back; `pairs.py items` adds them to `captions_all.jsonl` locally, and they get the same judge items.

## 4. Judges and prompts

### 4.1 Per-object judge

| key | model | how | venv | question languages |
|---|---|---|---|---|
| `qwen25vl_7b` | `Qwen/Qwen2.5-VL-7B-Instruct` @ `cc594898137f460bfe9f0759e9844b3ce807cfb5` | `guard.hf_verifier` (B-N1 model block, every snapshot file pinned) | B-N1 (transformers 4.57.6) | en, vi |
| `qwen3vl_8b` | `Qwen/Qwen3-VL-8B-Instruct` @ `0c351dd01ed87e9c1b53cbc748cba10e6187ff3b` | `guard.hf_verifier` | B-N1 | en, vi |
| `internvl3_s2` | `OpenGVLab/InternVL3-8B` @ `853e3a797a661694b1b8ece0cb72dc2b23e3dac9` | `guard.s2_verifier`: S2's instrument unchanged (`xv_ef1.verifier`, README loader, 12 tiles, shard pins) | S2 (transformers 4.51.3) | en |

- **Score rule.** S2's rule, through C's guard, imported unchanged (guard.py sha256 `5f930e96…`):
  - p = P(Yes + yes) / (P(Yes + yes) + P(No + no)) at the first answer position;
  - it is asked with the image, and with the question alone once per class (`guard.fill`).
- **The answer-position check** of `guard.hf_verifier` stops a run if the median yes + no mass over the first 20 questions is below 0.5.
- **Questions.**
  - **en:** S2's template, read from the pinned S2 prereg (sha256 `ac6404b6…`): `Is there {np} in the image? Answer yes or no.` Here {np} is S2's English noun phrase of the class. The question form is POPE's (Li et al., EMNLP 2023) with S2's suffix.
  - **vi:** `Trong ảnh có {np} không? Trả lời có hoặc không.` This is `scripts/pope_vi.py` `PROMPTS["vi"]` with its placeholder renamed (self-tested), and {np} is the lexicon class word. The answer words are có/Có against không/Không, the rule of `scripts/probe_existence.py`.
  - Neither wording is claimed as E's.
- **Vietnamese answer tokens without editing guard.py.**
  - `guard.hf_verifier` hardcodes the Yes/yes/No/no ids. `judge.retarget` overwrites, in place, the id lists that the verifier's `ask` closure reads. It checks through the closure that they are the same objects.
  - It refuses when the four first tokens are not distinct, and it resets the answer-position check for the new words.
  - S2's InternVL3 path builds its ids inside `xv_ef1.verifier`, which cannot be reached this way. So InternVL3 is asked in English only (judge Q5).
- **Snapshots on M3.** The lead reports these revisions registered and present on M3; this note could not check. The operator runs `lb.check_snapshot` (HF judges and generators, inside every mode) and S2's shard check (inside `guard.s2_verifier`) before any step counts. A missing snapshot is fetched at its pinned revision, and the fetch is logged.
- **One cache file per (judge, question language).** Each row holds (image, class, p_with, p_without), ids and numbers only.

### 4.2 Whole-caption judge (baseline)

- **Question.** `Does the following caption describe the image correctly? Caption: "{caption}" Answer yes or no.` The wording is written for this design, in S2's yes/no form, and is used for both caption languages.
  - It is not FLEUR's prompt. FLEUR's own rating prompt and score smoothing (LLaVA-1.5) are not run, and their exact text is TO VERIFY against FLEUR's repository before the paper describes the baseline as "FLEUR-style".
- **Mechanics.** It runs through the same `guard.fill`, with the caption id in the class slot. So it is the same judge and the same P(yes) rule as E; only the granularity differs. It is asked once with the image and once without, which gives a raw variant (p_with) and a subtracted variant (p_with − p_without).
- **Judges.** `qwen25vl_7b` and `qwen3vl_8b`. `internvl3_s2` is optional and runs only within the cap (§8).

## 5. Variants explored (all CPU, on the caches)

- Question language ∈ {en (3 judges), vi (2 HF judges)}.
- d ∈ {subtracted (p_with − p_without), raw (p_with)}. The raw arm is the no-subtraction ablation.
- λ ∈ {0, 0.025, 0.05, 0.1}.
- n̂ = the median distinct mentions over the E-dev-A base references of the caption's language that name at least one class (the bases of §3.1; 2 in Vietnamese and 1 in English in the dry run; recomputed by `score.py`).
- **Pooling.** E and the whole-caption baselines are each the mean over judges, excluding the caption's own generator. The pairs Qwen2.5-VL-7B ↔ `qwen25vl_7b`, Qwen3-VL-8B ↔ `qwen3vl_8b` and InternVL3-8B ↔ `internvl3_s2` count as the same model.
  - Reference captions are scored by all judges.
  - InternVL3-8B's LLM is Qwen2.5-7B, and Qwen3-VL is in the Qwen line: the shared lineage is stated, as in C.
- The whole-caption and embedding baselines have no tuning knobs.

## 6. Baselines

| scorer | kind | definition |
|---|---|---|
| `siglip2` | global, reference-free | image–text cosine of `google/siglip2-so400m-patch14-384`, at the revision recorded in Paper C's lists addendum. Text is padded to 64 tokens (model card; TO VERIFY). |
| `mclip` | global, reference-free | CLIP-S = 2.5 · max(cos, 0) with `scripts/clip_score.py`'s model (open_clip `xlm-roberta-large-ViT-H-14`, `frozen_laion5b_s13b_b90k`, fp32). Whether open_clip and these weights are on M3, and in which venv, is TO VERIFY; if absent, `mclip` is dropped and the paper says so. |
| `whole_raw`, `whole_sub` | whole-caption VLM judge (§4.2) | pooled as in §5 |
| `chair_loo` | reference-based, **context only** | −CHAIR_i (`rescap.chair.chair`) against the image's other Vietnamese references: for a pair, the references other than its base; for a model caption, all of them. Never a "best global" candidate. |

The best global baseline for each metric is the one of `siglip2`, `mclip`, `whole_raw` and `whole_sub` with the highest dev-A point estimate. Stage 2 freezes it.

## 7. Metrics and decision rule (fixed now; `score.py`)

### 7.1 Metrics

- **Pairwise accuracy per type** (§3.2) is the share of pairs ranked correctly.
  - A tie (|Δ| < 1e-12), or a caption without a score, counts 0.5, for every scorer.
  - For Δ-only types, the mean Δ and the share ranking the perturbed caption strictly lower are reported.
- **Kendall τ-b** (`scipy.stats.kendalltau`, variant b, since verified precision has ties) is computed between each scorer and the OIV7 verified precision. It uses the Vietnamese model captions with at least one verifiable mention, pooled over the four generators.
- **Uncertainty.** An image-cluster bootstrap, B = 2,000, `numpy.default_rng(0)`, with 95% percentile intervals. Differences between scorers use the same resamples.
- **Disclosure.** E extracts exactly the mentions that verified precision scores, so τ favours E partly by construction. The global baselines see the whole caption. The paper states this next to the τ table (judge Q8).
- **Reported, not gating:**
  - English rows;
  - the Vietnamese − English gap of bc accuracy, per scorer;
  - `ool_absent`, `delete`, `add_present` and `pad_control`;
  - per-judge rows, the raw arm, `chair_loo`, and the median yes + no mass per cache.

### 7.2 Pick (Vietnamese, dev-A)

1. **(question language, subtraction).** At λ = 0, take the pooled E with the highest τ-b. Ties go to en, then subtracted.
2. **λ.** Take the largest λ > 0 that meets both conditions, against λ = 0:
   - it raises `pad` accuracy by at least 0.05;
   - it raises the `pad_control` false-alarm share by at most 0.05.
   - If no λ passes, λ = 0 and the calibration claim is dropped.

### 7.3 Advance to stage 2

**ADVANCE** if all hold for the picked E:

| check | condition |
|---|---|
| **A1** (adapted from QQ34 E2; Q15) | Vietnamese bc accuracy of E − the best global baseline ≥ +0.10, 95% CI lower bound > 0 |
| **A2** (adapted from QQ34 E1) | Vietnamese τ-b of E − the best global baseline's τ-b ≥ +0.05 (point; CI reported) |
| **A3** (the scorer works at all) | E accuracy ≥ 0.70 on Vietnamese `swap` and on `add_absent` |

Otherwise the verdict is **FAIL**. In either case, if fewer than 40 images contribute Vietnamese bc pairs, `decide` returns **JUDGE** (the dry run found 43).

**Scope of this rule (CC-081, Q15; stage 1 only).**
- bc pairs favour E by construction: the pair differs by one lexicon object, and E asks about exactly that object. Every A1 row reports `ool_absent` beside it, and the paper states the by-construction advantage next to A1, as for τ (Q8). The 89 out-of-lexicon terms and their exact-name rule are disclosed there.
- Claims are scoped to objects within the 69-class lexicon.
- The stage-2 and test preregs either restore QQ34 E2 (out-of-lexicon pairs in the co-primary, pooled over 3 judges), or record a named deviation from the PI-approved plan with this reason.
- A2 is point-only here. Stage 2 and test restore QQ34 E1's 95% CI lower bound > 0.

### 7.4 After stage 1

- **ADVANCE:** write the stage-2 prereg for E-dev-B (one look) with the picked configuration frozen, including its best-global baseline. It suggests SESOI 0.10 (bc) and 0.05 (τ) and fixes them.
- **FAIL:** at most one more dev-A round, and only under a stage-1b note that lists everything seen here, within the 4 GPU-h cap in total. Then E stops (QQ34 §2.4).

### 7.5 Ledger

`score.py score` appends one JSON row per run. It holds the decision, every (language, scorer, metric) point, CI and count, n̂, and the sha256 of every input. It never holds a caption. It lists the judge caches used, which fixes the number of judges pooled. A per-object cache that lacks any needed item (a step stopped by the cap) is dropped whole and listed. Every variant scored is kept.

## 8. Budget (one RTX 3090)

- **Measured** (C DESIGN §8): Qwen2.5-VL-7B decodes at 0.70 s/image and InternVL3-8B-hf at 1.27 s/image; S2's InternVL3 verifier needs 1.17 s per item for both passes.
- **Assumed, as in C:**
  - 1.0 s (point) or 1.2 s (high) per with-image judge question for every judge;
  - 0.1 s per text-only question;
  - Qwen2.5-VL-3B and Qwen3-VL-8B decode at 0.7 and 1.27 s/image;
  - the Qwen3-VL speed is unmeasured.
- **Item counts** are from the dry run (§10). There are about 670 (image, class) items from pairs, plus about 30% from model captions, giving about 900. There are about 1,250 Vietnamese captions (222 bases, about 550 perturbed, 484 model) and about 600 English ones.

| step | computation | GPU-h point | GPU-h high |
|---|---|---|---|
| zero-shot decodes, 4 VLMs | 121 × (0.7 + 0.70 + 1.27 + 1.27) s | 0.13 | 0.20 |
| per-object, en | 900 × 3 judges × 1.0–1.2 s | 0.75 | 1.17 (+30% items) |
| per-object, vi | 900 × 2 judges × 1.0–1.2 s | 0.50 | 0.78 |
| whole-caption, vi | 1,250 × 2 judges × (1.0–1.2 + 0.1) s | 0.76 | 0.90 |
| embeddings (SigLIP2 + M-CLIP) | about 1,850 texts, 121 images | 0.03 | 0.05 |
| model loads (about 10 processes) | 2–3 min each | 0.40 | 0.60 |
| **required total** | | **about 2.6** | **about 3.7** |
| optional: whole-caption en (2 HF judges) | 600 × 2 × 1.1–1.3 s | 0.37 | 0.43 |
| optional: whole-caption vi, `internvl3_s2` | 1,250 × 1.2 s | 0.42 | 0.50 |

- **Hard cap: 4.0 GPU-h for stage 1.** This is QQ34 §2.4's E exploration budget, fixed in advance. The operator sums GPU time from the run records and stops the queue at the cap.
  - The optional steps run only if the running total plus their high estimate stays ≤ 4.0.
  - The lead's request was about 6–10 GPU-h. CC-081 (Q2) keeps QQ34's 4 h; more needs a PI amendment of QQ34.
- **CPU.** `pairs.py build`, `items` and `score.py` take minutes, and all three run locally.
- **Order on M3** (one model in 24 GB at a time):
  1. `decode`: qwen25vl_7b, qwen3vl_8b, internvl3_8b, qwen25vl_3b (B-N1 venv);
  2. the decodes copied back; `pairs.py items` locally; `items.jsonl` and `captions_all.jsonl` copied to M3;
  3. `objects`: qwen25vl_7b and qwen3vl_8b (en then vi, one process each, B-N1 venv), then internvl3_s2 (en, S2 venv);
  4. `whole --lang vi`: qwen25vl_7b, qwen3vl_8b;
  5. `embed`;
  6. the optional steps, within the cap;
  7. caches copied back; `score.py score` locally.

## 9. What is reused, and what is new

| reused unchanged | from |
|---|---|
| per-object P(yes) with and without the image, the answer-position check, the cache filler | `scripts/c_stage1/guard.py` (`hf_verifier`, `s2_verifier`, `fill`, `classes`, `key`, `delete`, `END`) |
| S2's instrument, English question and class map | `scripts/xv_ef1.py`, `manuscript/prereg/2026-10-18_tier3_S2.json` (pinned by guard) |
| model blocks, snapshot pins, venv, `short` prompt, LB decoder | B-N1 registration and `scripts/lb/decode_hf_vlm.py` (pinned by `decode_icl`) |
| XM-dev500 rule; the caption list of the n-gram scan | `scripts/c_stage1/build_memory.py` `split`, `dataset_captions` |
| test-image exclusion | `manuscript/prereg/2026-10-21_dev_pools/exclusion.json` (pinned by `decode_icl`) |
| OIV7 status rule and verified precision | `scripts/xm3600_oiv7.py` |
| Vietnamese existence question; CLIP-S | `scripts/pope_vi.py`; `scripts/clip_score.py` |

New in `scripts/e_stage1/`: the E-dev split and its refusal, the pair construction and English matcher, the answer-word retarget, the whole-caption item builder, the scorer, the metrics and the decision rule.

## 10. What was read before this note was written

- **Files and fields.**
  - Paper C's DESIGN and code, guard.py, xv_ef1.py, the S2 prereg's protocol fields, and the B-N1 model registry (ids, revisions, licences).
  - Paper A's N2 record, and the key structure of the OIV7 label and map files.
- **XM3600 counts, with no caption printed:**
  - per-image reference counts: 3,450 images × 2 and 150 × 3 in Vietnamese, 3,600 × 2 in English;
  - the XM600 membership of the 150 three-reference images (27 inside).
- **A local dry run** of the split and of the pair construction, with C's split rule and this note's code, on CPU. It printed counts only:
  - split sizes 600 / 250 / 250 / 2,500, and three-reference images 27 / 7 / 8 / 108;
  - 128 labelled E-dev-A images; per-type pair and skip counts; 669 (image, class) items from pairs; 77 Vietnamese bc pairs from 43 images, and 49 English from 30;
  - median mentions per reference: 2 in Vietnamese, 1 in English.
- **A synthetic smoke test of the scorer.** Random numbers stood in for the judge caches, and copies of base captions stood in for model captions. It checked that the code runs end to end. No judge, model or embedding ran; no number from it is a result.
- **Label rows printed while orienting.** One full OIV7 label row (present and absent MIDs) of one XM3600 image was printed while reading the file structure. That image is in XM600, Paper A's test set, which E never uses. E-dev-A label aggregates were also printed: 55 of the 128 labelled images carry both a present and an absent mapped class, with means of 2.29 present and 3.80 absent per labelled image.
- **The dry-run files** were written to a scratch folder and deleted. The dry run loaded E-dev-A references in memory to build perturbations; no caption was printed or inspected.
- **Never opened:** `data/ktvic_openviic_refs.json`, and the XM600 model outputs in `data/results/xm3600/` (only their file names were listed).

## 11. Open questions and the judge's rulings (CC-081: YES at 85% after edits E1–E3, applied here)

| # | question | ruling (default where unchanged) |
|---|---|---|
| Q1 | Paper A's three-reference set is mostly outside XM600 (§2.3: 7 in E-dev-A, 8 in E-dev-B, 108 in XM-test2500). Only reference object positions were read. | Fixed by E2 (§2.3): keep them in every set, primary analyses include them; E's and C's test preregs add a sensitivity analysis without the 108 test images. C's stage-2 prereg discloses 27 / 15 (7 + 8) / 108. |
| Q2 | Budget: QQ34 §2.4 fixed E's exploration at ≤ 4 GPU-h; the lead asked for about 6–10. | YES: hard cap 4.0 (QQ34 §2.4 item 3). Point estimate about 2.6; more needs a PI amendment. |
| Q3 | Power: E-dev-A gives about 77 Vietnamese bc pairs from 43 images. | Keep the 250/250 split required by QQ34's dev-A/dev-B rule; JUDGE if under 40 images. Alternative: 350/150. |
| Q4 | Overlap with C: E decodes C's `zs` backbones and asks C's guard question on XM-dev500, C's future dev-B pool. | YES, with the binding order of E3 (binding 5): disclosed in both papers, freshness protected both ways. |
| Q5 | Vietnamese questions use an in-place answer-id retarget of `guard.hf_verifier` (closure-checked) instead of editing the committed guard.py. InternVL3 (S2 path) is asked in English only. | As written. |
| Q6 | English is secondary: a head-noun matcher over S2's noun phrases, no synonyms, low recall. | English rows are reported and never gate. |
| Q7 | The whole-caption baseline uses this design's yes/no wording, not FLEUR's prompt. | Call it "whole-caption VLM judge"; say "FLEUR-style" only after checking FLEUR's repository. |
| Q8 | τ favours E by construction, because verified precision is computed on E's own mentions. | Disclose next to the table. A1 (bc) and A2 (τ) are both required. |
| Q9 | Self-preference: a judge scoring its own generator's captions. | Excluded from every pooled score (§5); per-judge rows reported. |
| Q10 | The out-of-lexicon map (COCO name = OIV7 display name) and `coco80_vi.json` terms are tooling. | Yes, as for Paper A's `vi_oiv7_map.json`. |
| Q11 | `delete`, `add_present` and `pad_control` have no faithful winner. | Δ-only rows; `pad_control` serves as the false-alarm guard of λ. |
| Q12 | Was the counts-only dry run of the split and pairs (§10) acceptable before this note? | Yes: no judge or model ran, and no caption was printed or inspected. |
| Q13 | Which images go to M3? | Only the E-dev-A pair images (about 121), not all of XM-dev500. E-dev-B goes after the stage-2 prereg (QQ34 §2.4 item 4). |
| Q14 | `oiv7_labels.json` is in git, so it is on M3 with test-image labels. | Fixed by E1 (§2.6): the operator removes it from M3 before E's first M3 step and records its absence; GPU modes refuse while it or an XM3600 annotation file is present, and hash only DESIGN, guard.py and clip_score.py; every label step runs locally. |
| Q15 | QQ34 §2.3 E2 puts the out-of-lexicon pairs inside the co-primary, pooled over 3 judges. A1 gates on bc only and makes `ool_absent` report-only; if the Vietnamese question wins the pick (§7.2), A1 and A2 pool 2 judges, since InternVL3 is asked in English only (Q5). | YES for stage 1 only, as a routing rule (§7.3 scope): `ool_absent` beside every A1 row, the by-construction advantage stated, claims scoped to the 69-class lexicon; stage 2 and test restore QQ34 E2 or name the deviation, and restore A2's CI lower bound > 0. The number of pooled judges is reported with every row. |

## 12. What this note does not do

- It registers no hypothesis, SESOI or verdict. The thresholds in §7 are stage-1 routing rules only.
- It judges, decodes and embeds no E-dev-B, XM600 or XM-test2500 image.
- It commits no output.
