# VSPS-J M0 PREREG: Vintern-1B-v3_5 single-probe yes/no-logit detection recall, cross-lingual (zero-shot vs 2-shot, M-HalDetect val)

Status: DRAFT for a one-judge read (tier REVERSIBLE, dev-explore, bar >= 90), 2026-10-31. Not committed.
Licence for drafting: CC-207 ruling 3 (GO-with-fixes 90, 3/3). This file closes CC-207 W1-W5 for M0 (map in section 12).
Nothing here licenses a GPU rental or any test-set use. The rental needs this read's GO, the PI's block funding (CC-207 Q5)
and a free slot under CC-207 ruling 8 / W11 (section 9).

Code: `scripts/vsps_j_m0/` = `m0.py` (plan, probe, score), `m0_stats.py` (section 6 statistics), `test_m0.py` (CPU
selftest, no weights, no data), `m0_job.sh` (GPU job); SUMS in that folder. Plan and id lists: this folder
(`m0_plan.json`, `*_ids.txt`, `fetch_images.txt`; SUMS here). Every number below marked [measured] was produced by
`python3 -I scripts/vsps_j_m0/m0.py plan` on the laptop on 2026-10-31 and is in `m0_plan.json`.

## 1. Construct (W1)

**Name:** Vintern-1B-v3_5 (verifier backbone, `rescap/vlm/registry.py` l.31) single-probe yes/no-logit detection
recall, cross-lingual. This is **not** the VSPS v1 verifier decision: there is no proposition extraction, no K=5
self-consistency, no support/contradiction probe pair and no three-way rule. Only one P(yes) per span is recorded, so no
v1 three-way verdict exists to report (the W1 clause on support/contradiction scores does not apply).

- **Model:** `5CD-AI/Vintern-1B-v3_5`, revision `b98f263eab246eb5269ade64edbdca8a887dc44d`. Pinned files (sha256):
  `model.safetensors` 296a16a6bf28e6d3f0fb9298deba70b3cfa1d7519f4aa326e2f862bf2e63be05,
  `modeling_internvl_chat.py` 4935c1f1d205167150d4449cbaf4bf340d8d5d0fd96ca97be5d15b26d489ead1,
  `conversation.py` 7e457a0fc08304deeb386ed1932e9db88dfbca888e0649ff76d488ae6c8aebfe,
  `config.json` 1c9ddcbef42ce4c672fefeb6c217be0ba05429f91ef1e3401cdb78eda17533fb. `m0.py` refuses any other.
  The pinned `config.json` maps its classes through the repo name, so `transformers` resolves the remote code via the
  cache's `refs/main` even when loading from a folder. The job writes `refs/main` = the pinned revision and loads by repo
  id with `HF_HUB_OFFLINE=1` (`m0.py check_model` refuses otherwise). Found and fixed in the CPU smoke (section 7.3).
- **Tiling:** registry value `max_tiles` 4 for the probed image (`get_vlm("vintern-1b")`), bf16 on CUDA.
- **Environment:** `transformers==4.51.3` (the repo's `requirements.txt` pin). `transformers` 5.22.1 cannot load the
  pinned remote code (`AttributeError: all_tied_weights_keys`, CPU smoke, section 7.3). The job also asserts torch
  2.15.0 and torchvision 0.29.2 (any +cu/+cpu build), numpy 2.5.4, pillow 13.0.0, timm 1.0.30 and einops 0.8.2. It refuses
  any other version and saves `pip freeze`.
- **Probe language:** the English M-HalDetect span inside the Vietnamese có/không template. No machine translation,
  so no MT model and no MT confound. The cross-lingual confound remains: a Vietnamese-tuned 1B model judges an English
  span. It is stated beside every number.
- **Span-to-question rule** (`m0.py question`): collapse whitespace; strip; strip trailing `. , ; : ! ?`; then
  `Có đúng là "<span>" không`. The adapter's suffix rule is then applied byte-identically (`m0.py instruct` =
  `vintern.py` l.314): `<question without a trailing ?>? Chỉ trả lời 'có' hoặc 'không'.`
- **Context loss:** each segment is probed alone, without the rest of the description. Pronouns and ellipsis ("They
  are ...") lose their referent. This is a limitation of the single-probe construct and is reported.
- **Any comparison with the <= 9B literature states that the model is 1B** (UNIHD, ZINA, the 8-9B span-F1 results).

## 2. Data (W3)

No re-fetch. M0 reuses the A-N3 pin `.session_backup/2026-10-19/HL_human_labels/dl_mhaldetect/`:
`val_raw.json` 2cbc7942f2ceafb0312f4f41b79390fe600605ffda9a9591fd2346213d0389af (the dev split),
`train_raw.json` 03b088d113d94e6f7ebd939fe2040d9fb968f26878b088da77ed8d885ae17624 (demonstrations and smoke only),
`LICENSE.md` (annotations CC BY-NC 4.0, Scale AI; images under the COCO/Flickr terms). `m0.py` refuses any other sha.
**Prior use:** A-N3 used the same labels for a different claim (Paper A secondary: metric precision vs human object
precision; reported NOT_SUPPORTED). M0 cites A-N3 and makes no claim about it.

Counts [measured]:

| | value |
|---|---|
| val records | 3,164 |
| val images | 786 |
| val spans by label | ACCURATE 11,770; INACCURATE 4,680; ANALYSIS 5,207; UNSURE 435 |
| label-eligible spans (ACCURATE + INACCURATE) | **16,450** |
| excluded: ANALYSIS / UNSURE | 5,207 / 435 |
| excluded: span with no word character | 1 (ACCURATE) |
| **eligible spans after both rules** | **16,449** (11,769 ACCURATE, 4,680 INACCURATE); 16,027 of them are on the 769 decoded images (section 3) |
| records without any span (not probed) | 2 |
| train records / images | 10,979 / 2,695 |

Text between labelled spans is not probed (1,034 unlabelled gaps with a word character in val, 12,349 characters,
under 1 % of the 1.44M characters).

**Bias stated beside every recall (W3):** in M-HalDetect, text that annotators did not mark as Inaccurate stays
Accurate by default. Missed hallucinations are therefore labelled Accurate. Recall is measured against the
**human-marked** Inaccurate spans. Some flags on "Accurate" spans may be real errors, so precision is a lower bound.

No new labels are made; no AI label is used as evidence. No M-HalDetect text enters the repo: `m0_plan.json` holds ids,
labels, counts and text sha256 only, and the GPU host reads the pinned JSON directly.

## 3. Custody (W4)

All inputs are pinned and checked by `m0.py plan` [measured]:
- Karpathy splits: recomputed from `data/datasets/karpathy/dataset_coco.json` (2fd99922) and checked equal to A-N3's
  `data/an3/mhaldetect_overlap.json` (fd97a3b0): val restval 599 / test 91 / val 96; train restval 2,027 / test 329 /
  val 339; train-val image overlap 27. Any mismatch is a FAULT.
- **A-T3 3,232** (CC-197 r9 list, file 5aaa479f, ids b0aefdb4, checked as in `a_t3.py` l.398): val 0, train 0.
- **KV-4,224:** no list file exists yet (MT4 PREREG M7). `m0.py kv4224` rebuilds it with
  `scripts/grl/id_counts.py counts()` on that script's own pinned inputs, without calling its `main()` (which rewrites
  the GRL folder), and checks count 4,224 and the ids pin 86d93863. Overlap: val 0, train 0. As expected: KV-4,224
  already removes A-touched ids, which include the A-N3 instance-gold keys.
- **UIT-ViIC train pool (PORTFOLIO l.185, owner L1-P3 pending a ruling):** `ut2532.txt` (288340b8, GRL folder):
  val 17, train 56. (UT-2,402 ⊂ UT-2,532.)
- **exclusion.json** (`manuscript/prereg/2026-10-21_dev_pools/exclusion.json`, c52a96d1; the refused spent
  evaluation sets of the dev-pool rule), val / train: Karpathy test 91 / 329; coco2500 44 / 173 and cv295 5 / 21 (both
  inside Karpathy test); CHAIR-500 10 / 30; POPE-500 7 / 33 (1 val inside Karpathy test); UIT-ViIC test 0 / 0. Union in
  val: 106 images.
- **Rule, fixed now (two classes):**
  - **Owned elsewhere, never decoded** (M0 is the later-registered set, l.185): A-T3 ∪ KV-4,224 ∪ UT-2,532. Dropped:
    **17 val + 56 train images** (`dropped_ids.txt`, 73 ids). Judge question 1 offers the alternative of keeping the 17
    (full split 786).
  - **Refused by exclusion.json, probed but held out:** these are spent evaluation sets. CC-207 W4 probes the 91
    Karpathy-test images and keeps them out of every operating-point choice; M0 treats the other exclusion.json lists
    the same way. Held out of the selection set: **106 val images** (`selection_excluded_ids.txt`). Held out of the demo
    and smoke pools: every listed train image.
  - **exclusion.json image_sha256** (KTVIC test, XM3600, cv295, CHAIR-500, UIT-ViIC test bytes): `m0.py probe` hashes
    every fetched image before the smoke. A byte match whose id is not already held out is a FAULT (expected none).
- **Probe set (full split):** 786 - 17 = **769 val images, 16,027 segments (4,605 Inaccurate)**. No other subsetting.
- **Selection set (every operating-point and threshold choice):** probe set minus the 106 held-out images = **663
  images, 13,813 segments, 3,993 Inaccurate**. This is the primary result. The 769-image full split at the same
  thresholds is reported beside it, together with the release counts in section 2.
- **Demo and smoke pool:** train images minus the 27 also in val, minus Karpathy test, minus every exclusion.json list,
  minus A-T3, KV-4,224 and UT-2,532 = **2,228 images**.
- **W25 near-duplicate filter: not run, open (judge question 2).** l.185 asks for it across all owners before any decode.
  M0's custody is id-level and byte-level (exact COCO ids, exclusion.json image sha256), not near-duplicate. The W25
  memory and SSCD features live on M1/M3 (`scripts/w25`, `scripts/c_t3/c_t3_neardup.py`), not on the laptop. The
  recommended default is to proceed without it: M0 trains nothing, tunes only tau_B on dev, and every M-HalDetect id is
  ledgered so later owners' W25 passes can drop them.
- **Ledger (prepared, not appended; the gatekeeper appends):** every M-HalDetect image is VSPS-J dev-touched under the
  PORTFOLIO l.185 image-level rule, so B4 (owner of restval) drops them: `dev_touched_ids.txt` = 786 val ∪ 2,695 train
  = 3,454 ids, including the 73 never decoded. The 91 Karpathy-test ids go to the tier-2 (spent, dev-confirm) ledger. The proposed lines are in
  `JUDGE_READ_REQUEST.md`.

## 4. Arms and the 2-shot path (W2, W5)

- **Arm A (zero-shot):** `m0.py probe(ad, pv, q)` with no demos. It passes exactly what `VinternAdapter.yes_no_logit`
  (`vintern.py` l.292, the path `scripts/gate_t05.py` ran) passes to `chat()`: `history=None`, automatic
  `num_patches_list`, the same suffix, `_yes_no_ids`, and P(yes) = yes-mass / (yes + no mass) on the first decoding step.
  Two changes, both on the read side: `max_new_tokens` 1 instead of 4 (only step 1 is read), and the raw yes+no mass is
  returned. The smoke checks equivalence with `yes_no_logit` itself (section 7).
  Inherited from the adapter and disclosed: `_yes_no_ids` takes the first token of "Có / có / Không / không" with and
  without a leading space, which includes the bare tokens "C" (id 34) and "Kh". P(yes) therefore also absorbs any
  C-initial first token. The smoke reports the decoded ids.
- **Arm B (2-shot, interleaved multi-image):** the same probe with two demonstration turns passed through the pinned
  `chat(history=..., num_patches_list=...)` (`modeling_internvl_chat.py` l.252-284). With `history` set, `chat()` does
  not prepend `<image>`, so every turn carries its own `<image>\n`. Placeholders are filled in order of appearance, so
  pixel values are concatenated demo 1, demo 2, query, and `num_patches_list` = [demo 1 tiles, demo 2 tiles, query
  tiles]. Demo turns: `<image>\n` + instruct(question(demo span)), answer `Có.` (Accurate) or `Không.` (Inaccurate).
  **Demo images use one 448 tile** (256 image tokens each; `m0.py demo_pixels`, the adapter's transform), to bound cost.
  The query image keeps the registry tiling. The CPU selftest checks placeholder count = `len(num_patches_list)`, tile
  order, tile sums, generate restore, P(yes) and mass on a fake model that applies the pinned placeholder rule.
- **Demonstrations (fixed now, never retrieved; C owns retrieval ICL):** from the demo pool, segments of 5-30 words,
  sorted by (record, segment), shuffled with seed 20261031; the first ACCURATE and the first INACCURATE from a different
  image. Their order is shuffled with seed 20261032. Result [measured, `m0_plan.json`]: (1) train record 4680 seg 9,
  image 168248, INACCURATE, 18 words, text sha a3710279; (2) train record 9230 seg 1, image 296224, ACCURATE, 12 words,
  text sha 02bf9436. The same two demos go in every arm-B prompt. They are the UNIHD / Self-Check few-shot baseline, cited
  as such and not claimed as a contribution.
- **If 2-shot cannot run** (smoke rule, section 7), arm B and its stop rule are dropped and arm A runs alone. No model is
  substituted.

## 5. Claim-type keyword rule and exclusions (W5), fixed now

- **Exclusion:** only ACCURATE and INACCURATE spans with at least one word character are probed. ANALYSIS and UNSURE are
  excluded and their counts reported (section 2).
- **Claim type** (`m0.py TYPE_RULES`, English, case-insensitive, whole words, **first match wins: count > attribute >
  relation > object**):
  - count: digits; one ... twelve, dozen(s), couple, pair, several, few, many, multiple, numerous, single, both, lone,
    group(s);
  - attribute: colour, size, material and state words (red ... purple, silver, gold(en), colorful, colored, dark, light,
    bright; large, small, big, little, tall, short, long, tiny, huge; wooden, metal, plastic, glass, stone, brick; old,
    young, new, empty, full, open, closed, wet, striped, round, square);
  - relation: spatial prepositions and interaction verbs (on, under, above, below, behind, beside, near, between, inside,
    next to, in front of, on top of, across, along, against, holding, riding, carrying, wearing, using, eating, playing,
    watching, looking at, sitting, standing, walking, lying, leaning, hanging, parked);
  - object: everything else (the "other" bucket).
- Probe-set counts [measured] (Accurate / Inaccurate): count 2,096 / 1,560; attribute 3,125 / 424; relation 2,322 /
  992; object 3,879 / 1,629. Per-type recall is descriptive only, with no decision attached.

## 6. Outcomes, operating point, statistics and decision (W5)

Positive class = INACCURATE. Score = 1 - P(yes). All choices below are on the **selection set** (663 images).

- **Arm A operating point (fixed):** flag iff P(yes) < 0.5. Its precision P_A and recall R_A are computed on the
  selection set.
- **Arm B operating point (rule fixed now; its value is computed after the probes):** flag iff P(yes) <= tau_B, where
  tau_B is the cut over distinct arm-B P(yes) values (ties grouped) with the **highest recall subject to precision >=
  P_A**. Among cuts with equal recall, the one with fewer false flags. If no cut reaches P_A, arm B fails (R_B = 0).
- **Primary quantity:** dR = R_B(tau_B) - R_A(0.5), in recall points.
- **Paired percentile bootstrap by image:** B = 2,000, numpy `default_rng(20261031)`, resampling the 663 selection-set
  images with replacement and keeping all segments of each image. P_A and tau_B are **re-selected inside every
  replicate**. 95 % CI = the 2.5th-97.5th percentiles. CIs are reported for dR, R_A, R_B, AUROC_A and AUROC_B.
- **AUROC:** Mann-Whitney with ties counted 1/2, Inaccurate vs Accurate, per arm.
- **Also reported:** precision at R = 0.80 (the best precision among cuts with recall >= 0.80) per arm, per-type recall
  at each arm's operating point, and the full 769-image split at the same P_A / tau_B with recall, precision and AUROC.
  Every recall carries the Accurate-default bias sentence (section 2) and the 1B / cross-lingual / context-loss
  qualifiers (section 1).

**Stop rules (program section 2, M0), applied to the selection set:**
1. **Few-shot:** KEEP iff point dR >= **+3.0** recall points (SESOI) **and** the 95 % CI lower bound of dR > 0.
   Otherwise few-shot leaves the plan (E1 drops "M0's 2-shot probe arm", E2 drops 2-shot probes). With arm B dropped,
   the verdict is N/A.
2. **Detector:** if point AUROC < **0.65** in both arms (arm A alone if B is dropped), the verifier is not a usable
   detector at this size, and E2 pivots to cross-family voting. CIs are reported beside it. CC-207 Q3: an English
   tier-3 set is reconsidered only if AUROC >= 0.65.

The decision is computed by `m0.py score` (`m0_stats.decide()`), once, on the complete run. `score` refuses an incomplete probe
file. Nothing is retuned after the probes. No probe is re-run to change a result.

## 7. Smoke and FAULT rules (W2)

### 7.1 GPU smoke, before any val image

50 train images from the demo pool (minus the two demo images), 2 segments each, seeds 20261033/20261034 (pinned in
`m0_plan.json` `smoke`). Both arms are run on them. Never val, never the demo images. Rules:
- **Tokens resolve:** `_yes_no_ids` non-empty, yes ∩ no empty, each id decodes to a prefix of có / không. Else FAULT.
- **Arm A:** every P(yes) finite; median yes+no first-token mass >= 0.5; >= 90 % of decoded first tokens are có/không
  first tokens; equivalence with `VinternAdapter.yes_no_logit` on the first 5 smoke segments, |dP(yes)| <= 1e-3. Both
  run the same forward pass on the same inputs, so the expected difference is 0 (CPU: 0.0). 1e-3 leaves room for
  non-deterministic bf16 CUDA kernels and is far below any effect on a 0.5 threshold or a rank. Any failure is a FAULT: the run stops, nothing is decoded on val, and an amendment follows.
- **Arm B:** the same finite / mass / token rules. Any failure, or an exception in the 2-shot path, means arm B is
  dropped; arm A continues.

### 7.2 During the run

A non-finite P(yes) is a FAULT and stops the run. A run stopped by FAULT, PROJECTION_STOP or CAP_STOP is never scored. Every such exit writes a STOP marker in the run folder, the cap is checked before each image, and `m0.py` then refuses to resume or score that run (as it does on any recorded stop, any non-finite P(yes) or a `probes.jsonl` that differs from its `.sha256`), while a crash with no marker may resume (CC-208 W1).

### 7.3 CPU smoke already run on the laptop (compatibility only, not evidence)

`~/.venvs/vsps_j_m0` (CPU torch 2.15.0+cpu, torchvision 0.29.2, transformers 4.51.3, numpy 2.5.4, pillow 13.0.0,
einops 0.8.2, timm 1.0.30; `pip freeze` saved beside the output, sha 18d2bc8b), float32, `--smoke-n 2` (2 train smoke
images, 4 segments, both arms). It ran on the **final code** (`m0.py` 9f81f899) with the final demos:
- tokens resolve: yes ids decode c / có / có / có, no ids kh / không / không / không;
- median mass: A 0.998, B 0.994;
- first-token text rule: 100 %;
- equivalence with `yes_no_logit`: max |dP| 0.0.
- **seconds per probe (CPU):** A 15.0, B 34.5 (ratio 2.3). An earlier run with the first demo draw gave A 9.3, B 31.7
  (ratio 3.4).
- Output: scratchpad `m0_cpusmoke2/smoke.json` (sha 894718a5), outside the repo; not used for any decision.

It also found the two load problems fixed in section 1 (`refs/main`, and transformers 5.22.1 incompatibility). This smoke ran on `m0.py` 9f81f899; the CC-208 W1 stop guard changed `m0.py` after it, with the probe path (`probe`, `run_smoke`) unchanged.

## 8. Cost, cap and the projection rules (W2)

- **Anchor (reused, W2):** `scripts/gate_t05.py` ran `yes_no_logit` on 600 Vietnamese probes:
  `data/results/gate_t05.json` `sec_per_probe` 0.413 s. Conditions: RTX 3090, adapter default `max_tiles` 6, KTVIC
  images, 4 new tokens, image load and tiling per probe.
- **Arm A at the anchor:** 16,027 x 0.413 s = **1.84 h**. M0 should be faster per probe: 4090, max 4 tiles, 1 new
  token, one tiling per image (about 21 segments per image).
- **Arm B (3-image prompt):** the demos add 512 image tokens. The CPU smoke ratios B/A = 2.3-3.4 are compute-bound
  upper bounds; on a GPU a 1B model at under 2k tokens is mostly overhead-bound.

| B/A ratio | Arm B (h) | A + B (h) |
|---|---|---|
| 1.5 | 2.8 | 4.6 |
| 2.0 | 3.7 | 5.5 |
| 3.4 | 6.3 | 8.1 |

  All rows use the 3090 anchor for A. If the 4090 halves A, the rows become 2.3 / 2.8 / 4.0 h.
- **The estimate does not guarantee a fit.** The two projection rules below decide, and nothing is changed to make the
  run fit.
- **Cap: 5 GPU-h** = wall time of the probe process from its first launch (`launch.json` t0) to exit, including model
  load and smoke, as in AMENDMENT_1 A4. Setup is outside the cap but is logged and paid: venv, weights (3.75 GB), 821
  COCO val2014 images, about 1 h.
- **Pre-val projection (new, protects the rental before any val decode):** after the smoke, projected =
  elapsed h + sum over arms of (val probes x smoke median s/probe) / 3600. If it is above 5.0, PROJECTION_STOP: no val
  image is decoded.
- **50-image projection rule (binding form, CC-206 style):** both arms are interleaved per image, so a stop leaves
  paired data. When the 50th val image in the fixed order (seed 20261035, `image_order_sha256` 4ed15aa8) is done:
  projected = elapsed h + sum over arms of (remaining probes x median s/probe over val images 2-50) / 3600. If it is
  above 5.0, PROJECTION_STOP.
- **Hard cap:** after each image, if elapsed > 5.0 h, CAP_STOP.
- **After any stop:** report it and write an amendment (for example, batching the probes of one image). Never a subset,
  never another model.
- **Cost:** about 5-6 h of rental at about 17,500 VND/h = about 90-105k VND (CC-207 ruling 7: the M0 block only).

## 9. Run, return and scoring

- **Slot (W11, CC-207 ruling 8):** the dates are non-binding. The M0 GPU block queues behind the A freeze (11-10), the B
  freeze (11-30) and the C / A-T3 / MT4 gates. VSPS-J slips, never A or B. M1 is not used. Per PI-1031c, the host is
  deleted after the pull.
- **Staging on the rented 4090:** a copy of the repo at the commit that holds this prereg (`rescap/`, `scripts/vsps_j_m0/`,
  this folder; `scripts/grl/` is used only by `plan` on the laptop), plus `val_raw.json` and `train_raw.json` (A-N3 pins; checked
  by sha). No host, IP or port is written in the repo.
- **Commands:**
  - `PY=<venv>/bin/python bash scripts/vsps_j_m0/m0_job.sh --selftest`
  - then `PY=... DATA=... IMAGES=... OUT=<outside the repo> bash scripts/vsps_j_m0/m0_job.sh`
- **What the job does:**
  - checks both SUMS and `transformers==4.51.3`, and runs the selftest;
  - fetches the pinned revision;
  - downloads the 821 images in `fetch_images.txt` from the public COCO server and writes `images.sha256`;
  - runs `m0.py probe` (smoke, projections, interleaved arms; resumable with the same command, the cap clock keeps its
    t0);
  - writes `probes.jsonl.sha256`.
- **Return:**
  - `sha256sum` on the host, scp to a new laptop folder, check the sha again;
  - delete the host folders and log it.
- **Scoring (laptop, once):** `~/.venvs/vsps_j_m0/bin/python -I scripts/vsps_j_m0/m0.py score --data <A-N3 folder>
  --out <run folder> --res <run folder>/m0_result.json` (numpy is not visible to the system `python3 -I`; the venv is
  the CPU twin of the GPU env: torch 2.15.0+cpu, torchvision 0.29.2, transformers 4.51.3, numpy 2.5.4, einops 0.8.2, timm
  1.0.30). The score path was exercised once on synthetic random P(yes) values (no model output) to check it runs
  (about 8 s for B = 2,000); that file was deleted. The result json holds numbers only; it enters the repo through the gatekeeper with its
  sha.

## 10. What this can and cannot claim

- **Can (dev-explore, English arm T-EN):** detection recall, precision and AUROC of a 1B Vietnamese-tuned VLM's
  single yes/no probe on English human-labelled sub-sentence spans. Also whether a fixed 2-shot prompt lifts recall at
  matched precision.
- **Cannot:**
  - anything about the VSPS v1 verifier decision, Vietnamese captions, or KTVIC;
  - any test-set or tier-3 claim (M-HalDetect val is dev, and its 91 Karpathy-test images are spent);
  - any >= 80 % recall claim (a design goal, PI-1031g, never a threshold).

## 11. Not covered here (CC-207 items that do not touch M0)

- **W6:** M0 uses none of the H1 3,700 records.
- **W9:** M0 cites neither retention 52.9 nor mirror 69.6, so `ret.py` is not needed here.
- **W7, W8, W10, W12:** later steps.

## 12. CC-207 fix map

| Fix | Where closed |
|---|---|
| W1 name, 1B, revision pin, span-to-question rule, probe language, no v1 verdict | section 1 |
| W2 l.214 corrected (gate_t05 ran `yes_no_logit`); anchor reused; 2-shot implemented with selftest; smoke with finite P(yes) and có/không rules; drop arm B on failure, never swap; cost for 3-image prompts; 5 GPU-h cap; 50-image rule | sections 4, 7, 8; `test_m0.py` |
| W3 A-N3 pin reused; 3,164 / 786 / 16,450 recounted; A-N3 cited; Accurate-default bias | section 2 |
| W4 overlap file reused and re-checked; A-T3 and KV-4,224 overlaps recomputed (0) and dropped, plus UIT-ViIC train pool (17 val / 56 train) dropped under l.185; 91 Karpathy-test images (and the other 15 exclusion.json val images) out of every choice; full split beside; ledger lists; W25 near-dup open | section 3 (ledger append by the gatekeeper) |
| W5 operating point; SESOI +3; paired image bootstrap B 2,000 seed 20261031; CIs for dR and AUROC; claim-type and exclusion rules; seed-fixed train demos without the 27 overlap images, never retrieved, cited as baseline | sections 4-6 |
