# Pre-registration: PASCAL-50S, a large-reference replication of the A4 ordering for Paper A (dated 2026-10-28)

- **prereg_id:** `2026-10-28_a_p50_kladder`. Directory `manuscript/prereg/2026-10-28_pascal50s/`.
- **Status (D-W13-6, as copied into A-N2):** REGISTERED only if the commit of this file, with the evaluator, the companion evaluator `scripts/pascal50s/p50x.py`, the companion registration `manuscript/prereg/2026-10-29_a_companion/RULE.md`, the job, the V20 table, the 1,000-ID list and the smoke list, precedes the first output of any run below. A file that is only locally frozen is EXPLORATORY. A file written at or after the first output is POST_HOC.
- **Kind:** a new registration. It **supersedes the PASCAL-50S part of B3** (`manuscript/prereg/2026-10-14_b3_licence_verification.md`, commit ca644df). B3 itself is not edited. The erratum is in §1.4.
- **Context only (CC-142 W2):** B3 l.30 states a direction for nocaps: b(k) and the verbosity slope "increase monotonically with k from k=1 to k=10 and instance labels". This file does not use nocaps (PI-1026ap Q3). B3 l.39 gives PASCAL-50S a role only, with no direction, so every rule below is new to PASCAL-50S.
- **Venue:** Paper A goes to SPIC in 12/2026 (CC-142 ruling 5: freeze 12-18). The earlier A freeze of 11-10 no longer applies. The run cutoff is 11-16 12:00Z (CC-142 ruling 8). With no decide file by then, A freezes with this test marked "not run" (§9.3).
- **Rulings:** CC-144 (W1–W13, rulings 1–13), CC-142 W2/W4/W6/W8, PI-1026ap (1)–(4), PI-1026az (licence, §1.4).
- **Source draft:** Ken K20, `manuscript/ken/K20_PASCAL50S_PREREG_DRAFT.md` (sha256 `3d4d3b72c6fc…756f`). Every judge-fixed item is marked "judge-fixed (CC-144)" (W11).
- **Code (§11):**
  - evaluator `scripts/pascal50s/p50.py`;
  - companion evaluator `scripts/pascal50s/p50x.py` (registration `manuscript/prereg/2026-10-29_a_companion/RULE.md`, CC-158 W1, CC-159);
  - job `scripts/pascal50s/p50_job.sh`;
  - lists `scripts/pascal50s/p50_1000_ids.txt` and `scripts/pascal50s/p50_smoke20_ids.txt`;
  - pins `scripts/pascal50s/SHA256SUMS`.

---

## 0. What the authors saw before writing (as A-N2 §12)

**Ken (K20 §0):**
- Paper A: §1 Table 1 and §7.2–§7.4.
- The B3, XM3600, G2B and A-N2 preregs.
- The UIUC PASCAL Sentences page. Ken read only the licence line and the file names, not the captions.
- `pascal50S.json`: streamed through sha256 only. It was never opened or stored.
- The VOCpatch tar: only its ID column was used.

**Writer (2026-10-28):**
- Re-fetched the UIUC page and the VOCpatch tar into an empty scratch directory. A script printed only counts and sha256 values, and both files were deleted afterwards.
  - Page sha256 `305741ea…42e3`: 1,000 `<img>` tags, 1,000 IDs, first `2008_000032`, last `2008_008755`. The sorted list has sha `a8539efb…4cb4`.
  - Patch tar sha256 `944e7d1d…6df6`. `trainval.txt` has 4,332 IDs, sha `c582af05…55e0`, and holds all 1,000 UIUC IDs.
  - The 20 smoke IDs are the first 20 of sorted(trainval − UIUC), equal to K20 §6.
- Did not fetch `pascal50S.json`.
- Read the code that is reused unchanged: `decode_hf_vlm.py`, `score_g2b.py`, `score_coco_probe.py` and `grl/common.py`.
- 2026-10-29 (companion writer, CC-158 W2): `pascal50S.json` was fetched once on the laptop into an empty scratch directory, its sha256 and size were checked against the §1.1 pin, and the unchanged `p50.py refcheck` was run on it (numbers only), before the §11 commit; the file was deleted at once. Result (`.session_backup/2026-10-29/a_x1_devcheck/p50_refcheck_local.json`): shape `records_image_id`, 1,000 keys of pattern `9999_999999.jpg`, 1,000/1,000 matched 1:1, 50 references for every image. No reference text was printed or stored. This departs from §6 ("on M3 only") and from §11 ("before any data step"); every rule for each n_refs shape was fixed before the counts were seen.

**Outputs:** no model output on PASCAL-50S exists or has been opened.

## 1. Data

### 1.1 PASCAL-50S (references)

- **Citation:** Vedantam, Zitnick & Parikh, "CIDEr: Consensus-based image description evaluation", CVPR 2015, pp. 4566–4575, DOI 10.1109/CVPR.2015.7299087, arXiv:1411.5726.
- **What the paper says it contains:**
  - "we collected 50 sentences per image for the 1,000 images from UIUC Pascal Sentence dataset";
  - "We ensure that each sentence for an image is written by a different subject".
- **Source.** The old official page is dead (DNS failure), `vrama91.github.io/cider/` returns 404, and Wayback returned 429. The only live copy is the authors' code repository:
  - `github.com/ramavedantam/cider` at commit `f281464c60d496b8fabb89a7a8c120f655a3a2bd`;
  - file `data/pascal50S.json`, 4,546,057 bytes, git blob `8a482f874a9a6ff5d7daea49327a9912ac8bcedc` (published by GitHub), sha256 `5384abf1340f7295d535b99453bc2313e521c111ad13ec257239a4d5b477ef42` (Ken-computed).
  - The evaluator refuses any other byte string (`refcheck`).
  - `pascal_candsB.json` and `pascal_candsC.json` are not used.
- **Unknown until the structure check (§7):** the key format, the number of references per image, and whether the 5 UIUC captions are among the references. The rules for each case are fixed in §3.2.

### 1.2 Images: the 1,000 UIUC PASCAL Sentences images = VOC2008 trainval

- **ID list:** `scripts/pascal50s/p50_1000_ids.txt` (committed; sha256 `a8539efb…4cb4`, see §0).
  - The 1,000 IDs are all in VOC2008 trainval and none are in VOC2008 test, so full XML annotations exist for the 20 classes.
- **Source:** `VOCtrainval_14-Jul-2008.tar` from the VOC2008 mirror at `thor.robots.ox.ac.uk`, 577,034,240 bytes.
  - No sha256 is published. The job writes the tar's sha256 to EVENTS **before extraction** (W8), and `stage` refuses a tar whose size or sha256 differs from that record.
  - Only the 1,020 needed JPEGs and the 1,000 XML files are read from the tar. The tar is then deleted.

### 1.3 Licences (verbatim, with URLs)

**(a) UIUC PASCAL Sentences captions.** These are not used as gold here; they are recorded because PASCAL-50S is built on this image set. Source `https://vision.cs.uiuc.edu/pascal-sentences/`, raw HTML:

> `The image captions are released under a <a href=" http://creativecommons.org/licenses/by/3.0/">CreativeCommons Attribution-ShareAlike license</a>.`

The text says "Attribution-ShareAlike", but the link resolves to CC BY 3.0. CC-144 ruling 1 holds that the difference does not matter here: both permit use with attribution, and ShareAlike binds only distributed adaptations, which aggregate numbers are not. Rashtchian et al. (2010) is cited, and the line is quoted as is.

**(b) PASCAL-50S captions.** No data licence statement was found. The paper says only (arXiv:1411.5726, l.150–151):

> "Our code and datasets are available on the author's webpages."

The repository's `license.txt` at f281464 reads, verbatim (permission part):

> Copyright (c) 2015, Xinlei Chen, Hao Fang, Tsung-Yi Lin, and Ramakrishna Vedantam
> All rights reserved.
>
> Redistribution and use in source and binary forms, with or without
> modification, are permitted provided that the following conditions are met:
>
> 1. Redistributions of source code must retain the above copyright notice, this
>    list of conditions and the following disclaimer.
> 2. Redistributions in binary form must reproduce the above copyright notice,
>    this list of conditions and the following disclaimer in the documentation
>    and/or other materials provided with the distribution.

This is a BSD-2 software licence. It does not mention data, so whether it covers `data/pascal50S.json` is ambiguous (CC-144 ruling 1).

**(c) VOC2008 images.** Source `https://www.robots.ox.ac.uk/~vgg/projects/pascal/VOC/voc2008/`, "Database Rights", verbatim:

> The VOC2008 data includes images obtained from the "flickr" website.
> Use of these images must respect the corresponding terms of use:
>
> - "flickr" terms of use
>
> For the purposes of the challenge, the identity of the images in the
> database, e.g. source and name of owner, has been obscured.
> Details of the contributor of each image can be found in the annotation
> to be included in the final release of the data, after completion of the challenge.
> Any queries about the use or ownership of the data should be addressed to the
> organizers.

The link "flickr terms of use" is `http://www.flickr.com/terms.gne?legacy=1`. The use here is academic only, nothing is redistributed, and the images stay on the m3-role machine (M1; PI-1029d, CC-155, CC-157) and are deleted after the run (CC-144 ruling 1).

### 1.4 Licence ruling, disclosure and B3 erratum

- **Ruling (CC-144 ruling 1, answered by PI-1026az, 2026-10-28).** PASCAL-50S is used for aggregate statistics only, and no caption or image is redistributed.
  - The PI contacted the dataset authors (Vedantam, Parikh) privately. **Written confirmation from the dataset authors was obtained (2026-10-28; on file with the corresponding author).**
  - The licence gate of K20 §1.4 is therefore closed for the run. The gate never blocked the commit of this file.
  - **Withdrawal clause, fixed now and not after the look:** if the dataset authors withdraw their confirmation before Paper A is submitted, the PASCAL-50S result is removed whatever its verdict, and the §9.3 text is used.
- **Disclosure sentence for Paper A's data-availability statement (W2):**
  > PASCAL-50S (Vedantam et al., 2015) was obtained from the authors' public repository (commit f281464), which carries a BSD-2 licence notice and no separate data licence; written confirmation from the dataset authors was obtained (2026-10-28; on file with the corresponding author); it was used for evaluation only, and no caption or image is redistributed.
- **B3 erratum (CC-144 ruling 13).** B3 overstates the PASCAL-50S licence status:
  - its line "`B3` Execution Gate Status: `UNBLOCKED (True)`" and its PASCAL-50S licence cells are authored text, hard-coded in `.session_backup/2026-10-14/r12_verify/build_pd4_q6_preregs.py` l.585, with no primary source;
  - the "Image Licence" cell holds a citation, not a licence;
  - its "Official Source" URL is dead.
  This file supersedes B3's PASCAL-50S part. B3's gate status is not inherited. B3's nocaps licence cells are also unquoted: any future nocaps use must quote them afresh.

## 2. Systems: the frozen A-N2 set

- **Models:** the 8 models of A-N2 §2, with hub ID, revision, dtype, batch size, attention and processor kwargs unchanged:

  | Model | Hub ID @ revision |
  |---|---|
  | llava15_7b | `llava-hf/llava-1.5-7b-hf` @ `b234b804…` |
  | llava_ov_7b | `llava-hf/llava-onevision-qwen2-7b-ov-hf` @ `0d506805…` |
  | qwen25vl_3b | `Qwen/Qwen2.5-VL-3B-Instruct` @ `66285546…` |
  | qwen25vl_7b | `Qwen/Qwen2.5-VL-7B-Instruct` @ `cc594898…` |
  | qwen3vl_8b | `Qwen/Qwen3-VL-8B-Instruct` @ `0c351dd0…` |
  | internvl3_8b | `OpenGVLab/InternVL3-8B-hf` @ `259a3b64…` |
  | idefics3_8b | `HuggingFaceM4/Idefics3-8B-Llama3` @ `fddb4ff7…` |
  | smolvlm2_2b | `HuggingFaceTB/SmolVLM2-2.2B-Instruct` @ `482adb53…` |

- **Prompts and decoding:** `short_en` (60 new tokens) and `detailed_en` (160 new tokens), greedy.
- **Decoder:** `scripts/lb/decode_hf_vlm.py`, sha256 `e2de1881…5ac4`, unchanged. It refuses to run if its own sha differs from the registration pin.
- **Venv:** `/root/venv-lb` (torch 2.5.1+cu121, transformers 4.57.6, accelerate 1.15.0). The decoder refuses other versions.
- **Runtime registration.** The decoder reads a `vsps.lb_prereg.v1` JSON. `p50.py register` builds it on the m3-role machine by copying A-N2's `schema`, `models`, `model_list`, `decode`, `decoder` and `venv` blocks unchanged from the pinned A-N2 JSON (sha `d5714e2b…`). It adds:
  - two sets, `p50_1000` and `p50_smoke20`, whose manifests (ID, file, image sha256) are written by `stage` on the m3-role machine;
  - runs `p50_<model>-<mode>` (at most 16) and `p50smoke_<model>-<mode>` (16).

  The self-test checks that the copied blocks are equal and that the decoder's own `load_prereg` accepts the result. This is the only departure from A-N2's mechanics (§5). The registration's sha256 goes to EVENTS.
- **Drop order** if the cap is exceeded (§6). A whole model leaves, i.e. both of its runs. Judge-fixed (CC-144 ruling 2):
  1. idefics3_8b
  2. llava_ov_7b
  3. internvl3_8b
  4. llava15_7b
  5. smolvlm2_2b
  6. qwen25vl_3b
  7. qwen25vl_7b
  8. qwen3vl_8b

  Runs are decoded in the reverse order (qwen3vl_8b first), so an overrun loses the next model in the drop order.
- **Minimum:** with fewer than **3 models** (6 runs, the size of G2B's LADDER) the outcome is **STOP (cost)**. This is a new rule, judge-fixed (CC-144 ruling 2).

## 3. Design and analysis

### 3.1 Reference rungs and matcher

- **k ∈ {1, 2, 5, 10, 20, 50}.**
  - Gold `refsk_randk` is the union of the object classes of k references drawn without replacement.
  - `refs50` (= `refs_all`) is the union over all of an image's references.
- **Matcher:** `score_coco_probe.en_classes(text, load_synonyms())`, applied to outputs and references alike, imported unchanged (A-N2 §4). Vocabulary: COCO-80.

### 3.2 Reference draw and the structure check (fixed before `pascal50S.json` is read)

- **Allowed shapes.** Before any decode, the first data step on the m3-role machine reads the file (W6) and accepts exactly three shapes:
  - a dict {key: [reference]};
  - a list of records, each with one ID field (`image_id`, `image`, `filename`, `file_name` or `img`) and either a `caption` string or a list field (`captions`, `refs`, `references` or `sentences`);
  - a COCO-style {`images`, `annotations`}.
- **Allowed key normalizations (W6):** basename (which also strips a class/ prefix), then strip `.jpg`/`.JPG`. Nothing else.
- **What `refcheck` prints and stores:** the shape, the key pattern (digits shown as 9), the key count, the n_refs histogram, and the match count against the 1,000 IDs. No text.
- **No 1:1 match → NOT_EVALUABLE (input).** No decode runs, and a PI line on nocaps follows (PI-1026ap(3)). An image is never dropped to make the keys match.
- **The draw (function `draw` in `p50.py`, called by `score`), on all 1,000 images before any output's content is used, then restricted to the analysis set:**
  - `numpy.random.default_rng(1)`;
  - for k in (1, 2, 5, 10, 20) in that order, for r = 1..20, for each image in ID order: `choice(n_refs_image, k, replace=False)`;
  - an image with n_refs < k takes all its references at rung k and makes no draw;
  - k = 50 uses every reference (S = 1).
- **Consequences of the order:**
  - the k = 1 rung equals `score_g2b.random_subsets(n_refs, 1, 20, 1)` (self-tested);
  - the other rungs are a different stream from G2B's k = 1..K loop (departure, §5).
- **Reported:** the number of images with n_refs < k at each k, and the n_refs minimum and maximum.

### 3.3 Analysis set, bootstrap, scores

- **Analysis set:** images whose caption is clean in every run of every kept model: a non-empty string that `clean_supervision.CJK_RE` does not match (A-N2 §5). Its size is reported. The same statistics over all 1,000 images are a sensitivity analysis with no verdict.
- **Bootstrap:**
  - 1000 draws: `numpy.random.default_rng(0).multinomial(N, [1/N]*N, size=1000)` over the analysis set in ID order;
  - paired, shared by every run and every gold;
  - 95% CI = percentiles 2.5 and 97.5.
- **Scores:** P, R, mixed F1 and M by `score_g2b.scores`, imported unchanged, averaged over the random subsets.
- **`slope[g](F)`:** `score_g2b.stat_slope`, the OLS slope of 100·F1_x on ln M_x over the runs x of family F.

### 3.4 Family

- **ALL:** every `short_en` and `detailed_en` run of the kept models, pooled (at most 16 runs). This is A4's form: N1-XM-4 took one slope over the 6 systems of three models pooled.
- **Per-model slopes (`PAIR_m`):** descriptive only, with no verdict (CC-144 ruling 6).

### 3.5 Rules, verbatim

**A4 = N1-XM-4.** `manuscript/prereg/2026-10-14_xm3600_predictions.md` §2.1 item 2:

> - **`N1-XM-4 (Ordering)`**: $\text{slope}(\text{refs1\_randk}) < \text{slope}(\text{refs\_all}) < \text{slope}(\text{oiv7\_verified})$.

The same rule in `2026-10-14_xm3600_predictions.json` → `a_N1_sign_predictions.relative_form_predictions.P3_slope_ordering`:

> `"slope(refs1_randk) < slope(refs_all) < slope(oiv7_verified)"`

**G2B-O2.** `manuscript/prereg/2026-10-18_g2b_qwen3vl_ladder.md` §9:

> | **G2B-O2** | secondary | cv295, uv231 | the verbosity slope rises at every added reference, k = 1..5 | `slope[refs2_randk](LADDER) - slope[refs1_randk](LADDER)` sign_gt_0; `slope[refs3_randk](LADDER) - slope[refs2_randk](LADDER)` sign_gt_0; `slope[refs4_randk](LADDER) - slope[refs3_randk](LADDER)` sign_gt_0; `slope[refs_all](LADDER) - slope[refs4_randk](LADDER)` sign_gt_0 | H3 P6 and COCO-2500 P1 (k-step form) |

**G2B §8 verdict rules** (the lines used):

> - `sign_gt_0`: PASS if ci95_lo > 0; FAIL if point <= 0; else INCONCLUSIVE
> - `compound`: FAIL if any part is FAIL; else NOT_EVALUABLE if any part is NOT_EVALUABLE; else PASS if every part is PASS; else INCONCLUSIVE
> - `not_evaluable`: NOT_EVALUABLE if the analysis set is empty or a statistic is undefined (a system with M_x = 0, or fewer than 2 distinct M_x in a family)
> - `counting`: Kill rules count FAIL only. INCONCLUSIVE is reported as inconclusive and never as support. Earlier preregistrations scored sign and ordering claims on point estimates; 'not FAIL' here is that criterion, so the outcomes can be compared.
> - `multiplicity`: No correction; every prediction is reported separately, per dataset, with its CI.

### 3.6 Predictions on PASCAL-50S (every change from the sources is listed in §5)

| ID | Tier | Statement | Statistic and rule |
|---|---|---|---|
| **P50-A4** | primary (replicates A4) | slope(refs1_randk) < slope(refs50) < slope(voc20), on the V20 vocabulary (§4) | part 1: `slope[refs50\|V20](ALL) - slope[refs1_randk\|V20](ALL)` sign_gt_0; part 2: `slope[voc20\|V20](ALL) - slope[refs50\|V20](ALL)` sign_gt_0; compound |
| **P50-A4r** | primary only if the label rung is dropped before the look (§4.4) | slope(refs1_randk) < slope(refs50), COCO-80 | `slope[refs50](ALL) - slope[refs1_randk](ALL)` sign_gt_0 |
| **P50-O2** | secondary (replicates G2B-O2) | the slope rises at every added reference, k = 1→2→5→10→20→50, COCO-80 | `slope[refs2_randk] - slope[refs1_randk]`; `slope[refs5_randk] - slope[refs2_randk]`; `slope[refs10_randk] - slope[refs5_randk]`; `slope[refs20_randk] - slope[refs10_randk]`; `slope[refs50] - slope[refs20_randk]`, all (ALL); each sign_gt_0; compound |
| **P50-NS** | no prediction | the sign of the slope at every rung (COCO-80 and V20, and voc20) | reported with CI only |

- **One verdict rule:** the three-level `sign_gt_0` on the paired difference, with `compound` (CC-144 ruling 4).
  - The original A4 was scored on point estimates (Paper A §7.2). By the `counting` line, "not FAIL" is that criterion. "not FAIL" is written next to each part for comparison with A4 and is not a second verdict.
- **Not evaluable:** `not_evaluable` applies to each family. A V20 family with a model at M_x = 0, or with fewer than 2 distinct M_x, gives P50-A4 NOT_EVALUABLE, and P50-A4r then gets no verdict (W5).
- **Thresholds:** no new SESOI, no equivalence band, no magnitude threshold (CC-144 ruling 5).
- **Multiplicity (CC-144 ruling 6):**
  - primary family {P50-A4 (2 parts)}, or {P50-A4r (1 part)} if the label rung was dropped before the look;
  - secondary family {P50-O2 (5 parts)};
  - one dataset, one system family (ALL);
  - no correction (G2B `multiplicity`);
  - no kill rule counts P50-O2.
- **Descriptive contrast (W3):** whenever P50-A4 is primary, the COCO-80 contrast `slope[refs50](ALL) - slope[refs1_randk](ALL)` is reported with its CI, without a verdict.
- **Exchangeability:** each reference of an image was written by a different subject (§1.1). File order may still follow collection order, which is why the draw is random. There is no N2-type verdict check.

## 4. The VOC-2008 label rung (V20)

### 4.1 Gold

- For each image, the gold is the set of V20 classes with at least one `<object>` in `Annotations/<id>.xml` of `VOCtrainval_14-Jul-2008.tar`.
- Objects with `difficult = 1` or `truncated = 1` **are included**, because the object is in the image. Judge-fixed (CC-144 ruling 7, Q6).
- An XML object name outside the 20 classes counts as an unreadable XML (§4.4(c)).

### 4.2 V20 vocabulary and map (frozen here; `p50.py` constant `V20`)

| VOC2008 | matcher COCO-80 class | VOC2008 | matcher COCO-80 class |
|---|---|---|---|
| aeroplane | airplane | diningtable | dining table |
| bicycle | bicycle | dog | dog |
| bird | bird | horse | horse |
| boat | boat | motorbike | motorcycle |
| bottle | bottle | person | person |
| bus | bus | pottedplant | potted plant |
| car | car | sheep | sheep |
| cat | cat | sofa | couch |
| chair | chair | train | train |
| cow | cow | tvmonitor | tv |

- **Verification:** all 20 right-hand names are classes of `score_coco_probe.load_synonyms()`. CC-144 verified this (80 classes, 0 missing), and the evaluator self-test checks it on every run. So §4.4(b) cannot fire.
- **Disclosed gap (§10, W10):** the word "aeroplane" maps to no class. The matcher is not changed.

### 4.3 Gold and scores on V20

- `refsk_randk|V20` = `refsk_randk` ∩ V20.
- `voc20` = the gold of §4.1.
- Output mentions are also restricted to V20, so M_x of the V20 family counts V20 mentions.
- F1 is computed by the same `score_g2b.scores`.

### 4.4 When the label rung is dropped

The label rung is dropped, and P50-A4r replaces P50-A4, if any of the following holds **before the look**:
- (a) the §4.2 table is not committed with this file;
- (b) one of the 20 names is not a matcher class and no rename was approved before the look;
- (c) an XML file of the 1,000 images is missing or unreadable. `stage` records this as `label_rung` in `stage.json` before any decode.

K20's item (d), fewer than 2 distinct M_x, is **deleted as a trigger** because it depends on outputs (W5, CC-144 ruling 8). Its case is handled by the `not_evaluable` rule of §3.6. The rung is never dropped after the look.

## 5. Departures from the source rules (the verbatim blocks of §3.5 are not edited)

| Source | There | Here | Why |
|---|---|---|---|
| A4 | `oiv7_verified` (verified Open Images V7 labels, 82 classes) | `voc20` (VOC2008 labels, 20 classes), all golds of the comparison restricted to V20 | PASCAL has no OIV7 labels; VOC labels are complete only on their 20 classes |
| A4 | `refs_all` = 2–3 references | `refs50` = every reference (~50) | the data |
| A4 | 6 XM3600 systems (3 models × 2 prompts), Vietnamese | family ALL, at most 16 A-N2 runs, English | the set frozen by CC-142; English comparison rule |
| A4 (W3) | Vietnamese captions and the Vietnamese matcher (`vi_objects`) | English captions and references, English matcher `en_classes` (COCO-80) | PASCAL-50S is English |
| A4 (W3) | `refs1_randk` at XM3600 was the expectation over each image's references, verbatim (`2026-10-14_xm3600_predictions.json` → `gold_density_Gbar_eval600.refs1_randk.description`): "expected 1-reference gold size averaged across each image's 2-3 Vietnamese references" | random draws, `default_rng(1)`, r = 20 (§3.2), as G2B and A-N2 | 50 references make the expectation over single references an average of 50; the registered G2B/A-N2 draw is used instead |
| A4 (W3) | part 1 (refs1 < refs_all) on the full vocabulary | part 1 of P50-A4 on V20 | the comparison with voc20 needs one vocabulary; the COCO-80 contrast is reported descriptively whenever P50-A4 is primary (§3.6) |
| A4 | scored on point estimates | three-level `sign_gt_0` (see `counting`) | one rule for every replication |
| G2B-O2 | k = 1..5 in steps of 1, family LADDER, cv295 and uv231 | k = 1→2→5→10→20→50, family ALL, PASCAL-50S | the k grid of the task |
| G2B/A-N2 | K = 4, r = 20, draw loop k = 1..K | k ∈ {1, 2, 5, 10, 20}, r = 20, draw loop over that list; n < k takes all references | the k grid; possible images with fewer than k references |
| A-N2 | cv295 and uv231en; COCO instance gold | PASCAL-50S; ~50 references and VOC labels | new set |
| CC-142 W4 / K20 §6 (cap) | cap = smoke throughput × 1000 × n_runs × 1.5; a run is stopped at 1.5 × s_m × 1000 | cap_run = 1.5 × (o + 1000·s), with s from the slice stamps after the warm-up slice and o the measured fixed cost of a run (load, warm-up slice, parity slice); the run timeout is cap_run (§6) | the unchanged decoder's wall time includes model load, which a per-image rate over 20 images would multiply by 50; s and o separate the two. Confirmed, CC-159 ruling 4 |
| A-N2 | registration JSON committed with its set manifests | runtime registration built on the m3-role machine from the A-N2 JSON (blocks copied unchanged) plus manifests written at extraction | image sha256 values exist only after the VOC tar is fetched on the m3-role machine |

## 6. Cap, machine and data hygiene (CC-142 W4, CC-144 W7/W8)

- **Smoke:**
  - images: 20 VOC2008 trainval images **not** among the 1,000. The rule is sorted(`trainval.txt` of the patch, sha `c582af05…55e0`, minus the 1,000 UIUC IDs), first 20. Frozen list `scripts/pascal50s/p50_smoke20_ids.txt`: `2008_000002 2008_000003 2008_000007 2008_000008 2008_000009 2008_000015 2008_000016 2008_000019 2008_000021 2008_000023 2008_000026 2008_000027 2008_000028 2008_000033 2008_000034 2008_000036 2008_000037 2008_000041 2008_000042 2008_000045`;
  - every model runs both prompts with its registered configuration, on the m3-role machine (CC-142 W4/W8);
  - smoke outputs are used for timing only, never scored, and deleted right after timing;
  - each smoke run has a timeout of 3600 s. A smoke run may fault twice (any non-zero exit, the timeout included); its partial output is deleted and it is rerun from the start. At the third fault its model leaves (KM), with no replacement. Only models with both smoke timings enter the plan.
- **Measured time per run (`p50.py timed` / `run_cap`; this definition is fixed now):**
  - `timed` stamps each "slice k/n" line of the unchanged decoder;
  - s = (time of the last slice − time of the first slice) / (20 − first slice size), i.e. seconds per image with batch loading, after the first (warm-up) slice;
  - o = smoke wall time − 20·s. This is the fixed cost of a run: model load, first slice and the decoder's batch-1 parity slice. Weight download is not counted;
  - cap_run = 1.5 × (o + 1000·s);
  - cap_m = the sum over the model's two runs.
- **Ceiling: 8 GPU-h, smoke and all fault time included** (CC-144 ruling 12 Q7, judge-fixed):
  - `gpu_seconds.tsv` logs the wall time of every GPU process, failed ones included;
  - models are kept in the drop order (§2) while smoke_spent + Σ cap_m ≤ 8 GPU-h;
  - fewer than 3 models → **STOP (cost)**;
  - images are never dropped: all 1,000 are kept (PI full-dataset rule).
- **During the runs:**
  - each run's timeout is its cap_run. A run that reaches it is **FAULT (time)**: the model leaves (KM), with no rerun and no replacement (W7);
  - a run whose cap_run would take the ledger over 8 GPU-h is not started: the model leaves, with no replacement;
  - more than two infrastructure faults on one run (§7): the model leaves, with no replacement.
- **Projection (Ken; not a measurement, not binding):** 4.62 GPU-h is A-N2's upper bound for 526 images × 16 runs, not a timing. Scaled to 1,000 images × 1.5 it gives ~13 GPU-h > 8, so 2–4 models will probably leave.
- **Dates:** the m3-role machine, from the joint commit with the companion (CC-158 W1); cutoff 2026-11-16 12:00Z unchanged. If that commit has not landed by 11-08 12:00Z, P50 may run only with a judge-read job version without the p50x lines (CC-159 ruling 4). The start date is scheduled by the operator and is not machine-checked; the job's guard refuses any machine id other than m3 (CC-159 W1).
- **Cutoff, machine-checked:** the job checks the clock at its start and before every GPU process. At or after 2026-11-16 12:00Z (CC-142 ruling 8) it writes the decide file as "not run", deletes the data, and stops; §9.3 applies. This holds for `score` too.
  - P50 never displaces B-2 or B-1 (CC-142 W4): the guard refuses while a B-1, B-2 or C-EN process runs, while the GPU is busy, or while any other job lock exists.
  - Before the run, the operator checks the disk of the m3-role machine for the A-N2 snapshots (113.6 GB), the 577 MB tar and the outputs. The job refuses to fetch the tar with less than 2 GB free, and refuses to fetch a missing snapshot with less than 20 GB free.
- **Data hygiene (W8):**
  - the VOC tar sha256 goes to EVENTS before extraction;
  - images, XML, `pascal50S.json` and raw decodes are on the m3-role machine only, under `$NCS_DATA`, which the 30-minute backup never pulls;
  - after `score`, the job deletes them and writes the empty listing and the time to EVENTS;
  - git receives aggregates only (as B3 §3).
- **8-gram check (W4):** before any file leaves the m3-role machine, `p50.py ngram` counts the 8-grams it shares with `pascal50S.json`. A positive control (one reference against all references) must hit.
  - A decode file with 0 hits is copied to `/root/outputs/p50/preds/`, with its sha256.
  - A decode file with ≥ 1 hit never leaves the m3-role machine. Only its sha256 and the aggregates leave, and it is deleted with the data. A hit is not a verdict input.
  - The decide file must show 0 hits before it is copied out.
  - The gatekeeper's repository scan covers OpenViIC/KTVIC only, which is why this check is part of the evaluator.

## 7. One look, and reruns after faults

- **The look (W6, CC-144 ruling 9):** the first read of the content of any `p50_*` output, by the evaluator or by any person or tool. That read is `p50.py score`, followed in the same job by `p50x.py score` (the companion, `manuscript/prereg/2026-10-29_a_companion/RULE.md`), whose read of the same outputs is part of this one look.
  - The structure check of `pascal50S.json` (§3.2) is not the look. It runs first, before the smoke, and prints numbers only.
  - The reference draw runs inside the committed evaluator and uses only the per-image reference counts.
- **Committed before the look:** this file, the evaluator with its sha256, the companion evaluator `p50x.py` and its registration, the job, the V20 table, the smoke list and the 1,000-ID list, and the draw rule (§3.2).
- **Scored once,** after every kept run has finished and the local backup of `preds/` matches its SHA256SUMS. `score` refuses if a decide file exists.
- **Score-stage faults (CC-159 W2, fixed before the look):**
  - once `p50.py score` has written its decide file, the cutoff never fires: no "not run" record replaces a scored result, and the job only delivers;
  - P50's decide file is 8-gram-checked and copied out **before** the companion runs;
  - `p50x.py` gets at most 2 attempts, counted in EVENTS. After the second failure, or if its decide file has an 8-gram hit (that file stays on the machine and is deleted with the data), the companion is recorded as `{"status": "FAULT (code): companion not run"}` and the deletion proceeds. A companion defect never blocks P50's registered result;
  - an empty analysis set gives a NOT_EVALUABLE companion record, not a fault.
- **FAULT reruns** are allowed only while the faulted run's output is unopened, and only for infrastructure faults:
  - (i) the process dies, OOM, the machine is lost, or the rental expires;
  - (ii) an input sha (image, snapshot, decoder) differs from its pin;
  - (iii) an output lacks images because of a write or transfer error.

  The rerun uses the same configuration; the decoder resumes at its next unfinished slice. Every failed and rerun second counts toward the 8 GPU-h. A run may fault twice at most; at the third fault the model leaves (KM), with no replacement.
- **FAULT (time) is not rerun** (W7).
- **Smoke faults** follow §6: at most two per smoke run; at the third the model leaves.
- **Never rerun for content:** language, cap hits, odd captions or results.
- **Provenance:** a run whose provenance differs from the registration (prereg ID or sha, decoder sha, manifest sha, packages, a dirty tree, IDs) is handled as A-N2 KD. It is recorded as a deviation, and its model leaves the verdict family.

## 8. Nearest work

- **Vedantam et al. (2015, CIDEr)** is the nearest prior work.
  - They collected PASCAL-50S because more sentences per image are needed for reliable automatic evaluation.
  - They found that most metrics agree better with human consensus as the number of references grows from 1 to ~50.
- **What differs here:** this test measures no agreement with humans. It measures the sign and order of the object-F1 slope on ln M as the gold becomes more complete with k. It is the replication of Paper A's A4/G2B-O2 on 1,000 images the group has not seen, with up to 50 references.
- **Also cited:**
  - Rashtchian et al. (2010), ACL Anthology W10-0721 (the image set);
  - Everingham et al. (2010), IJCV 88:303–338, DOI 10.1007/s11263-009-0275-4 (VOC labels).

## 9. Branch texts, written before any output (Paper A §7.4; inserted as written once there is a verdict)

**9.1 Replicated (P50-A4 PASS, or P50-A4r PASS if the label rung was dropped).**
> On PASCAL-50S (Vedantam et al., 2015), 1,000 images not used elsewhere in this paper, with up to 50 independent references per image, the registered ordering replicated: the slope of object F1 on ln M under one reference lies below the slope under all references[, which lies below the slope under the VOC-2008 labels on the 20 VOC classes] (PASS; [values]; n = [clean images], [m] systems of the frozen A-N2 set). The rise at every added reference (k = 1, 2, 5, 10, 20, 50) was [PASS/INCONCLUSIVE/FAIL at step(s) …]. The sign of each slope was not predicted. The images and captions have been public since 2008–2015 and may be in the pretraining data of these models; they are unseen by us, not necessarily by the models.

**9.2 Not replicated (any part of P50-A4, or of P50-A4r, FAIL).**
> On PASCAL-50S the registered ordering did not replicate: [part] was FAIL ([value]). We report this as a failed out-of-sample replication of the ordering claim of Section 7.2; the confirmatory claim of this paper is restricted to the XM3600 and second-backbone tests, and the [failing part] is listed in Table 1 as FAIL. The images and captions have been public since 2008–2015 and may be in the pretraining data of these models; they are unseen by us, not necessarily by the models.

**9.3 Not testable (INCONCLUSIVE, NOT_EVALUABLE, STOP (cost), not run by the cutoff, or withdrawn).**
> The registered PASCAL-50S replication [was inconclusive: the interval of [part] includes 0 / could not be evaluated: [reason] / was not run: [the compute cap of 8 GPU-hours left fewer than three systems / it did not finish by the registered cutoff] / was withdrawn: the dataset authors withdrew their confirmation of use before submission]. It carries no result and does not count for or against the ordering claim.

- **Every branch:** Table 1 gets a new row, with the verdict copied from the decide file.
- **If the label rung was dropped:** 9.1 must not say "replicates on a new dataset"; it says "for the reference ladder only".

## 10. Risks (disclosed limits; nothing here changes a rule)

1. **Pretraining exposure:** VOC2008 images and PASCAL captions have been public since 2008–2015 and may be in all 8 LVLMs' training data, like uv231's exposure label. A PASS is a replication on images unseen **by the group**, not by the models (the 9.1/9.2 sentence).
2. **Cap hits at 160 tokens (Paper A §7.3):** Qwen3-VL-8B and Idefics3-8B reach the cap on every detailed caption, so M is compressed into short and detailed clusters and the slope is close to a short-vs-detailed contrast. This is disclosed and not corrected (W10).
3. **The "aeroplane" matcher gap:** `en_classes` maps "aeroplane" to no class (plane and jet map to airplane), and PASCAL references may use the British form. This lowers airplane recall against the voc20 gold. It is disclosed and the matcher is not fixed (W10, CC-144 ruling 7).
4. **The 8 GPU-h cap** will probably remove models (§6), narrowing ALL and widening the CIs.
5. **V20 is narrow:**
   - 20 classes, and the images were chosen per class (50 per class), so the class distribution is skewed and "person" dominates;
   - part 2 of P50-A4 may be INCONCLUSIVE for lack of mentions.
6. **Saturation at large k:** from k = 20 to 50 the COCO-80 union may barely change. The 20→50 step of P50-O2 is then near 0: INCONCLUSIVE, or FAIL if the point is ≤ 0. This is a real risk for P50-O2, not a design error.
7. **Unknown file structure:** keys and reference counts can lead to NOT_EVALUABLE (input) (§3.2).
8. **The official source is dead:** the only live copy is the code repository. Its commit and sha are pinned here and must be printed in the paper.
9. **The English matcher** has never been checked on PASCAL-style captions. There is no matcher check with a verdict.

## 11. Files, pins and order of work

- **Committed together, in one commit, before any data step:**
  - this file;
  - `scripts/pascal50s/p50.py`, the evaluator: `--selftest`, `refcheck`, `stage`, `register`, `timed`, `plan`, `budget`, `ngram`, `score`. Numbers only;
  - `scripts/pascal50s/p50x.py` and `manuscript/prereg/2026-10-29_a_companion/RULE.md` (the companion, CC-158 W1);
  - `scripts/pascal50s/p50_job.sh` and its stub test `scripts/pascal50s/test_p50_job_paths.sh`;
  - the two ID lists;
  - `scripts/pascal50s/SHA256SUMS`, which pins this file, the evaluator, the companion evaluator and registration, the job, the lists, the decoder, the A-N2 JSON and every module the evaluator imports.
- **Job order on the m3-role machine:**
  1. lock, cutoff check and guard;
  2. **import check first** (`p50.py imports`);
  3. SHA256SUMS and the self-test;
  4. `refcheck`;
  5. VOC tar sha to EVENTS, then `stage`;
  6. `register`;
  7. snapshot pins;
  8. smoke;
  9. `plan`;
  10. decodes;
  11. 8-gram check;
  12. then, after the local backup matches: `score` → 8-gram check and copy of the P50 decide → `p50x.py score` (at most 2 attempts, §7) → 8-gram check of the p50x decide → deletion.
- **Before the commit (W13, CC-142 W2):** a single-judge diff-and-code read of this file and the evaluator (`--selftest`, patch = tree, SUMS), by 11-05. The gatekeeper commits by 11-07.
- **Paper A text (W12):**
  - the sec7 l.88 comment cites this file instead of "licence gate passed";
  - the visible text says "planned" until this file is committed, then "registered <date>";
  - the data-availability statement takes the §1.4 sentence once the result is used.

## 12. Answers to Ken's questions (K20 §11; CC-144 ruling 12)

1. **Licence:** ruling 1, answered by PI-1026az (§1.4).
2. **One verdict rule:** yes.
3. **Family:** pooled ALL; PAIR_m is descriptive.
4. **Minimum number of models:** 3.
5. **Drop order:** as drafted.
6. **Difficult and truncated objects:** included.
7. **Smoke and FAULT time:** both count within 8 GPU-h.

**Cap definition (§6, §5 cap row):** confirmed, CC-159 ruling 4. It replaces the literal formula of CC-142 W4 and CC-144 ruling 11 / W7; the cap, the cutoff and the drop order never move (CC-155 W3).
