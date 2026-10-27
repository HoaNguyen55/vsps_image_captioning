# Paper C, English arm (C-EN): pre-registration of the one-look test on COCO Karpathy test and NoCaps val

**Label: TEST, ONE LOOK PER SET.** Ruled by CC-121 (GO-with-fixes W1–W11). No English image is decoded, embedded or scored, and no test set is staged, before this file, its lists and the code of §13 are committed by the gatekeeper.

| field | value |
|---|---|
| Paper | C (retrieval in-context captioning), registered English extension; never a standalone paper (CC-107 r10) |
| Authority | CC-107 r5, r6, W2, W3; CC-111 W8, W9; CC-113 W3–W9 (as amended by CC-115 W4); CC-115 W6; CC-118 W6; CC-120; CP-116 W2; PI-1026b, PI-1026i, PI-1026l, PI-1026n, PI-1026r, PI-1026s, PI-1026t |
| C's test prereg (carried over) | `manuscript/prereg/2026-10-25_c_test/PREREG.md` sha256 `acecd6527217c5c59b84917aa1571cfa8b2e50b7879be38d2e305ef91df6363f` (`PT` below) |
| C's frozen configuration | `manuscript/prereg/2026-10-22_c_stage2/frozen_config.json` sha256 `2f0c32be7720b672f6e4aae229aba69da8742e0f9e32d34c5137e985ea36aa16` |
| Pinned lists (this folder) | `cen_memory_allowed.tsv` `175907e2…` (112,322 rows), `cen_coco_test.tsv` `67555b28…` (5,000), `cen_coco_kval.tsv` `f7d8369f…` (5,000), `cen_nocaps_val.tsv` `6add90eb…` (4,500), `cen_nocaps_vg1000.txt` `f8044b5e…` (1,000), `lists_record_coco.json` `0e264dd1…`, `lists_record_nocaps.json` `9e2928fe…`; producer `scripts/c_en/cen_fetch.py` (`lists`, `nocaps-list`), committed with the fetcher (CC-120) |
| Code | `scripts/c_en/` (§13), `SHA256SUMS` there |
| Machine | M3 only (CC-115 W4; PI-1026r). Verified by `/root/.vsps_machine_id` = `m3` and the committed HEAD in every M3 step |
| Written | 2026-10-26/27 on the laptop, CPU only. No English image has been opened by this study. The list producers read ids, file names, splits, coco_url and licence ids only; caption fields were parsed by the JSON loader but never used, printed or written |

## 0. Bindings

1. **CC-107 r5 is fixed, not re-decided here.** SESOI +2.0 CIDEr-D; k, order and τ from C's frozen configuration; the two backbones at their pinned snapshots; T1/T2 as direct translations; arms ret, rand, zs; PTB CIDEr-D; a fixed order over the two sets; one look per set; no dev evaluation; no English tuning of any kind.
2. **One look per set** (PT binding 2, binding 9). Each set is decoded once, scored once and decided once. No configuration, threshold, metric, set or rule changes after any English test output exists. No person or agent reads a test caption, ledger row or score before that set's decide has run; monitoring uses counts, times, GPU-s and return codes only.
3. **No English result changes any Vietnamese claim of C** (CC-107 r3), and no Vietnamese result is re-read in its light.
4. **No dataset caption and no host or address in any committed file; no prompt text in this file** (the translated templates live in `cen_decode.py`, as C's in `decode_icl.py`). Outputs (captions, embeddings, feature caches, ledgers, the caption store) are never committed; C-EN commits scores, ids and sha256 only.
5. **Nothing in this file is set from an English test set.** The SESOI and every threshold come from CC-107 r5 and PT.

## 1. Preconditions

### 1.1 Before this prereg is committed
1. The judge panel has read this file, `scripts/c_en/` and the lists, and the gatekeeper's 6/8-gram caption scan and identity/host grep find 0 hits.
2. The fetcher and the lists are committed (CC-120 r1); `cen_nocaps_val.tsv` and `cen_nocaps_vg1000.txt` reproduce `6add90eb…` and `f8044b5e…` from the NoCaps captions file at sha256 `2e8071fc…` and the vg-mamf cohort file at `a21e1138…` (CC-120 r5).
3. All selftests of §13 pass on the laptop (synthetic data only).

### 1.2 Before any M3 step
1. HEAD on M3 equals the gatekeeper commit; tracked tree clean; `SHA256SUMS` here and in `scripts/c_en/` verify (checked by every entry point, §13).
2. `/root/.vsps_machine_id` reads `m3`.
3. The venvs equal their freezes: `venv-lb` `685ffe2a…` (decode, SigLIP2, verifier), `/root/vsps/.venv` `7332d343…` (scoring: pycocoevalcap 1.2, wheel `083ed791…`; openjdk 11.0.32.1), and a features venv `venv-cenfeat` built on M3 from the committed freeze `manuscript/prereg/2026-10-27_c_en/cenfeat_venv_freeze.txt` (sha256 `1a639a50adf550c50c6dfe284146e279b2a2bf2a716ade743e9eb357ccbf0778`, the laptop's C stage-1 lists venv: torch 2.5.1 CPU, ImageHash 4.3.2; pHash/dHash/SSCD, no GPU) and verified against `FREEZE_FT` before POOL (CC-121 r7, W8). Each block checks only the venvs it uses.
4. No other GPU process on M3 during a GPU step (G-RL pilot interleaved, never concurrent with a test decode, PI-1026r(2)).

## 2. Frozen configuration (carried over unchanged)

Read only from `frozen_config.json` (`2f0c32be…`) through `scripts/c_stage2/stage2.py` `frozen()`:

| item | `qwen25vl_7b` | `internvl3_8b` |
|---|---|---|
| k | 8 | 4 |
| order | first | last |
| prompt tail | T1 | T2 |
| guard τ | −∞ (no guard) | 0.10 |

Also unchanged: the snapshots and revisions (Qwen2.5-VL-7B `cc594898…`, InternVL3-8B-hf `259a3b64…`, Qwen3-VL-8B verifier `0c351dd0…`, SigLIP2 so400m `e8e48729…`), the B-N1 batch sizes, dtypes and processor kwargs, greedy decoding with 60 new tokens, `N_EX` = 8, the retrieval near cut `NEAR_COS` = 0.92, the near-duplicate rule (min(pHash, dHash) ≤ 10 and SSCD ≥ 0.5, mirrored hashes, or byte-identical; `build_memory.py` `HASH_MAX`, `SSCD_MIN`), the rand seed `paperC|rand|<set>|<image id>`, the guard score s = P(yes | image) − P(yes | no image) with S2's question template, and the deletion rule with its zero-shot fallback.

**Translated, not tuned (CC-107 r5).** The prompt header, example line and tails T1/T2 are direct English translations of `decode_icl.py` HEADER/LINE/TAILS, fixed in `scripts/c_en/cen_decode.py` (`EN_TEMPLATE_SHA256` = `b329e57a62d67a5afa62ff04503ed30992028839eb65284c3c6cae93a64ed713`, asserted by its selftest). The zero-shot prompt is the committed `scripts/evaluate.py` `PROMPTS["short_en"]` (sha256 `0cdbdf77…`), the English counterpart of `short`, as decoded by A-N2 and G2-B (§12 item 3b). The guard's object matcher is the committed English COCO-80 matcher (`scripts/score_coco_probe.py` `en_classes`, synonyms `data/coco_probe/chair_synonyms.txt` `b685537b…`), the class phrase is "a"/"an" + the COCO class name, and the deletion separators and function-word end list are translations of `guard.py` SPLIT and `rl_reward.function_end`.

**The guard is an English port (CC-121 r6, W6).** τ = 0.10 was selected with the Vietnamese matcher v2 on Vietnamese dev (KTVIC dev299). The English side uses A's COCO-80 matcher (`chair_synonyms.txt` `b685537b…`), which shares 24 of its 80 classes with S2's 112-class map; the class phrase is the mechanical "a"/"an" + class name, kept unchanged as ruled; SPLIT and the function words are translated. All of it was fixed before any English ret or rand output. Known gaps: "a skis" and "a scissors" as phrases, and "men" unmatched. Its calibration is untested in English. The InternVL3 τ = −∞ row (§7) is printed beside the frozen τ = 0.10 row wherever the latter appears.

## 3. Sets

### 3.1 Primary: COCO Karpathy test, full 5,000
- `cen_coco_test.tsv`: the 5,000 `split == "test"` images of `dataset_coco.json` (`2fd99922…`), sorted by cocoid; it equals `exclusion.json` `ids.coco.coco_karpathy_test` (asserted).
- References: the first 5 `sentences[*].raw` per image in Karpathy order (the repo's pre-existing English rule: A-N2 prereg, `score_g2b.coco_context`, `crosslingual_gap.py` "the first 5 COCO captions of an image, in Karpathy's order"); 10 of the 5,000 have a sixth reference, which is not used. Fixed before data; it gates nothing else (CC-121 r8).
- No test-side exclusion: nothing was tuned on English data, so there is no dev set to be near (CC-107 r5 "no dev evaluation"). Near-duplicates are removed on the memory side (§4).

### 3.2 Secondary: NoCaps val, full 4,500
- `cen_nocaps_val.tsv`: the 4,500 `images` of the official NoCaps v0.1 val captions file (nocaps.org, Drive id `1zrsLhT94nazJ5h-LleHsU4AojHBqpcA0`, sha256 `2e8071fc…`, as vg-mamf recorded it), sorted by id, with `domain` (417 in / 2,670 near / 1,413 out, the file's own labels).
- Images: the NoCaps `coco_url` proxy (`s3.amazonaws.com/nocaps/val/…`) returns 403. Each image is fetched as `https://open-images-dataset.s3.amazonaws.com/validation/<open_images_id>.jpg`, the official CVDF Open Images host, by the official `open_images_id` (asserted `file_name == <oid>.jpg`); vg-mamf used the same source. Accepted by CC-120 r6; disclosed: the bytes or resolution may differ from the copy the dead proxy served.
- References: all 10 captions per image, as released (the official NoCaps protocol).
- **Sensitivity (PI-1026b):** the same estimand on the 3,500 images outside vg-mamf's stratified 1,000 (`cen_nocaps_vg1000.txt`), reported beside the full 4,500 and never replacing it.
- Per-domain rows (in/near/out) are reported, non-gating.

### 3.3 Protected only (never decoded): Karpathy val, 5,000
- `cen_coco_kval.tsv`. It is the KV pool, owned by D and since PI-1026l by the G-RL paper. It is hashed and feature-extracted for the memory-side near-duplicate pass only, then deleted; no model output is ever produced on it.

## 4. Memory (CC-113, PI-1026i)

1. **Candidates:** Karpathy train + restval, 113,287 images, minus every `exclusion.json` (`c52a96d1…`) coco id: 231 uitviic_test, 372 chair500, 367 pope500 = 965 refused, leaving **112,322** (`cen_memory_allowed.tsv`; reported beside 113,287).
2. **Fetch refusals (byte level, CC-113 W4, CC-120 r9):** a memory image whose sha256 equals any `exclusion.json` `image_sha256`, or any Karpathy test, Karpathy val or NoCaps val sha256 recorded by the hash-only pass, is refused in memory and never written; its id and the matched set are recorded and reported as N = 112,322 − r.
3. **Unreadable:** a memory image without features is dropped, never retried (LISTS_ADDENDUM rule, `build_memory.cmd_lists` `memory_groups`).
4. **Near-duplicate drops (CC-113 W6):** C's rule (§2), against the union of Karpathy test, NoCaps val and Karpathy val features, computed on M3 on CPU (`build_memory.near`, unchanged).
5. **Clustering:** `build_memory.clusters` (union-find under the same rule, byte-identical included) on the kept images; members sorted by cocoid; clusters ordered by their smallest cocoid and named `e000000…`; **members[0]** is the smallest cocoid.
6. **Retrieval vector:** members[0]'s SigLIP2 vector (fp16, L2-normalised, batch 64, in pinned list order).
7. **Shown caption:** members[0]'s first Karpathy sentence (`sentences[0].raw`, whitespace normalised), one source only, so C's "own dataset's member, else first member" rule reduces to members[0] (`decode_icl.shown`).
8. **Disclosed (PI-1026i):** D's UT pool (2,402 images: 1,545 train, 857 restval), since PI-1026l the G-RL paper's, is inside the candidates and kept.
9. The counts after each of steps 2–5 are written to the memory record before any test query is embedded.

## 5. Arms, retrieval, decoding

- Per (set, backbone): `ret`, `rand`, `zs` at the frozen k, order and template; `cen_` run ids; **12 decodes** (2 sets × 2 backbones × 3 arms). No fix arm, no blind arm.
- Examples: `build_memory.exemplars` unchanged (top-8 by cosine, ties by cluster id; rand 8 from the clusters under the near cut; a cluster at cosine ≥ 0.92 to the query is never shown).
- Decoding: the committed LB decoder (`lb.make_generate`, `decode_slices`, `write_output`), greedy, 60 new tokens, fixed batch slices, resumable.
- Guard: InternVL3's `ret` and `rand` are guarded at τ = 0.10 (Qwen3-VL-8B verifier, `guard.hf_verifier` and `guard.fill` unchanged); Qwen gets no verifier pass (PT §4). The Qwen3-VL answer-position stop is final for the set (PT §7.6): InternVL3's frozen arms are then incomplete and the set gives no verdict.
- Image decode: strict PIL decode; any failure of a test image in an image-opening step is a JOB STOP back to the judge (there is no named truncated-file list for these sets).

## 6. Scorer and bootstrap

- **Scorer:** pycocoevalcap 1.2 `PTBTokenizer` (Java) and `Cider` (CIDEr-D), ×100, df over the scored set's own references. Decision column `cider_ptb`. Venv `/root/vsps/.venv` (`7332d343…`).
- **Scored sets:** `coco_test_5000`, `nocaps_val_4500`, `nocaps_val_3500` (without vg1000); each with its own df and its own bootstrap matrix (PT §6.2, §6.3).
- **Bootstrap:** paired image bootstrap, B = 2000, percentile 95% CI, `numpy.random.default_rng(0).integers(0, n, (B, n))` drawn fresh per scored set; image order = the pinned TSV order (ascending id), filtered for the 3,500. Pooling: per-image differences averaged over the two backbones, then resampled.
- **Length:** mean PTB tokens of the final captions, the English analogue of C's syllable count (CC-121 r9).

## 7. Hypotheses and decision rule (CC-107 r5; fixed now)

Δ_m,i = `cider_ptb`(ret_m at τ_m, i) − `cider_ptb`(rand_m at τ_m, i); pooled Δ_i = ½(Δ_qwen,i + Δ_internvl,i).

| | P1-EN (primary) | S-NC (secondary, fixed order) |
|---|---|---|
| set | COCO Karpathy test 5,000 | NoCaps val 4,500 |
| estimand | mean pooled Δ_i | mean pooled Δ_i |
| pass | point > **+2.0** (SESOI) **and** 95% CI lower bound > 0 | the same rule |
| length rule L | either backbone \|len_ret − len_rand\| / len_rand > 0.10 on the 5,000: a pass is recorded as "PASS, not separated from length" | reported on the 4,500 only |
| sensitivity | — | the 3,500 without vg1000; per domain |

- **One rule for both sets (CC-107 r5; CC-121 r5).** It was fixed after C's XM-a result was known and is stricter than C's XM-a rule (lower bound > 0 only, from PR2 §8), so it can only be conservative.
- **Fixed order (gatekeeping, α = 0.05 each, family-wise 0.05):** the NoCaps claim "the gain transfers to NoCaps val" is made only if P1-EN passes and S-NC passes. **The NoCaps block is decoded, scored and decided whatever P1-EN shows** (as PT's XM block); the order gates the claim sentence only, not the run.
- **Reported, non-gating:** per-backbone Δ_m with CIs on every scored set; ret − zs and rand − zs, pooled and per backbone (descriptive); guard rates (neighbour-only, rejected, deleted, fallback) for InternVL3.
- **Registered secondary (PT §8.4 analogue):** InternVL3 ret − rand at τ = −∞ on each set, "detected" iff CI lower bound > 0; under a separate decide key that no gate or claim reads; printed after the frozen τ = 0.10 row.
- **No rescue:** a failed P1-EN is not rescued by NoCaps, a sensitivity, a per-backbone row, the τ = −∞ row or a domain.

## 8. Reporting rules
- Every registered row is reported with its value and CI, whatever the outcome.
- P1-EN fails: "the retrieval gain C found in Vietnamese was not detected on COCO Karpathy test", with the number; no post-hoc English analysis is offered in its place (CC-107 r3, PT §10).
- English results are reported within language only, never as a cross-language difference.

## 9. Order of work on M3 and kill rules

1. **Hash-only pass (`cen_fetch.py fetch`):** coco_test, coco_kval, nocaps_val; bytes hashed in memory, never written, no decode.
2. **Memory fetch:** only after the three records are complete; refusals of §4 items 1–2.
3. **POOL (GPU, cap 3 GPU-h):** SigLIP2 vectors of the memory; measured-rate guard (t − t0)/(n − n0) from the first embedded image's record, first projection at 5,000 images, re-projected every 10,000, STOP if the projection exceeds the cap (CC-113 W8).
4. **FEATS (CPU, no GPU held):** pHash/dHash/mirrored/SSCD of the memory (SSCD weights `9f26bd4c…`); then each protected set in turn (Karpathy val, Karpathy test, NoCaps val) is staged by `--stage` (sha equal to its record), feature-extracted and deleted, one at a time (Karpathy val is never staged again). **CC-121 W5:** any FEATS exit other than BLOCK DONE is followed in the same session by `cen_chain.sh cleanup feats <reason>` (the chain does this itself) before any other M3 job; the cumulative CPU wall time across calls is logged; a second timeout, or a total over 24 h, goes to the judge, and nothing is re-run without a judge line; no CPU CAP_STOP; no G-RL or CC-119 job runs while a protected set is staged.
5. **BUILD (CPU):** §4 steps 3–5 and 9. The laptop then makes the memory caption store from the mirrored `cen_memory.json` and uploads it (sha recorded on M3).
6. **SMOKE (GPU, cap 0.5 GPU-h, CC-113 r5):** the six arms of both backbones decode 16 memory images (the first 16 clusters' members[0]) queried against the memory (the 0.92 near cut removes each image itself), and InternVL3's items go through the verifier; a record of counts only (captions, empty, hit_max, items, verifier rows); nothing is scored; the smoke outputs are deleted, then the memory images. **Pass rule (CC-121 W7):** 96 captions (16 images × 6 runs), 0 empty, verifier rows equal to items, and no exception. Anything else is a STOP to the judge, and the COCO block refuses to start without a passing `smoke_record.json`. A failing smoke may justify only a crash or format fix, through a judge re-read and a new commit; it never changes a prompt, N_NEW, the guard, the matcher, the class phrases, a template or a threshold.
7. **COCO block, then NoCaps block** (whatever COCO shows): the laptop makes the block's reference subset and uploads it; the images are staged by `--stage`; then query embed, exemplars, 6 decodes, InternVL3 items + verifier, score, decide once; mirror, sha-confirm, delete the block's images and references (after NoCaps also the caption store); record times and shas. No G-RL or CC-119 pilot runs on M3 while any `cen_<test-set>/images` exists (CC-120 r4); the chain refuses to start a step while any other tmux session runs.
- **Kill rules:** the test GPU cap (§10) counted as job wall time with an open record and heartbeat (PT §12, CC-103b W4); every step under `timeout` for the time left; at most 3 attempts per step, then JOB STOP; the test cap is one shared 25 GPU-h budget across COCO and NoCaps, and a test-family cap stop is final for the rest of the family: during COCO, COCO gives no verdict and NoCaps is unrun, both reported incomplete; during NoCaps, NoCaps gives no verdict (CC-121 W4; `cen_job.sh` CAP_STOP_test); the judge may extend the cap only before any partial output is read; a crash resumes with the same code; any refused id or sha, any Karpathy val image outside FEATS, or any file outside its list on disk is a STOP to the judge (CC-113 W8); one run only per step.

## 10. GPU budget and cap (CC-115 W6)

Measured on M3 at C's test (job logs, `.session_backup/machines/M3/root/outputs/c_test/job_*.log`; `gpu_seconds.tsv` ov 16,597 s / 2,001 images, xm 17,646 s / 2,500): 2.30 and 1.96 GPU-h per 1,000 images (4 arms), about 2.1 overall. Per image-arm: Qwen 0.69 s (OV) / 0.40 s (XM), InternVL3 1.24 s / 1.30 s.

| block | basis | expected (3 arms) | at the ruled 2.1 GPU-h / 1,000 (4 arms) |
|---|---|---|---|
| COCO 5,000 | OV rates (conservative) | ≈ 8.6 GPU-h | 10.5 |
| NoCaps 4,500 | XM rates (Open Images, as XM3600) | ≈ 6.6 GPU-h | 9.5 |
| **test total** | | **≈ 15.2** | **20.0** |
| **test cap (hard)** | 20.0 + 25% margin | | **25 GPU-h** |
| POOL | SigLIP2 at 0.03 s/img × 112,322 ≈ 0.9 | | cap **3** (CC-115 W4) |
| SMOKE | | | cap **0.5** |

Priority if the cap binds: the COCO block first. A test-family cap stop is final for the rest of the family (§9 kill rules). A POOL rate-guard STOP is a cap stop (exit 124), never retried. CPU steps hold no GPU and are not counted against any GPU cap; FEATS (SSCD on CPU over about 112k memory plus 14.5k protected images) is estimated at about 4–9 h wall from C stage 1's CPU rate, under a 24 h operator timeout that is not a cap stop (no ruling sets a CPU cap).

## 11. Data, licence, staging

- Download (HEAD sample of 300 per source, 2026-10-26): memory ≈ 18.4 GB (stored until BUILD), Karpathy test ≈ 0.81 GB, Karpathy val ≈ 0.81 GB, NoCaps val ≈ 1.41 GB (hash-only, then staged twice for FEATS and the block). Network total ≈ 26–27 GB; disk peak ≈ 20 GB.
- Every file is hashed on arrival; per-file sha256 TSVs and done markers are mirrored by gpu_backup and listed in the run record.
- **Hash-only records, pinned (CC-121 W2)**, all complete at head `780ac71f748c34ff5d3075a6b37667c90683ccd3` with 0 refused, `stored: false`:

  | set | record_sha256 | done.json sha256 | completed (UTC) | bytes |
  |---|---|---|---|---|
  | coco_test | `614afa1b7cf63bde693fc9692b1699d47ba527d396b7a1216d031b1d50018fdf` | `6b3c4d75af05cc7d18a5e074fd863135d5f9c31e5398ac73926251215fe4f686` | 2026-10-26T17:38:31Z | 820,306,454 |
  | coco_kval | `8c93f306f24588fb6e66eed0a8ba2ba97e61adf901ddf5ab614b37d5b677ee1c` | `fc4c2942a25bd6e0554087e0f76e901d5959bbe911523a6f9c41cf9015fd47f4` | 2026-10-26T17:46:43Z | 812,848,612 |
  | nocaps_val | `fbbcd21ccd8e036e5d1a94bb0fa143538882ceec62ba76a1e9104d31f321cb33` | `e19eb75edc45137573dd3e0839901357e678adefd8dbdc9e300fecb9e1b863f2` | 2026-10-26T17:53:51Z | 1,418,236,279 |

  The record pins are in `cen_fetch.RECORD_PINS`; `--stage` refuses a record at any other sha and refuses before this prereg is in HEAD at its `SHA256SUMS` line (CC-121 W9). Before every `--stage` the chain compares the mirrored record with its pin and logs the result; no `--stage` is ever run by hand.
- **Memory fetch (CC-122 X2):** recorded 112,320 and r = 2: ids 388662 and 397819 (sha256 `fcc1fd100ed50e30ea87b9d84597cb40876c76d955716fc9dd6e936787faf181`) are byte copies of Karpathy-test 578492, refused and never written, so N = 112,320, reported beside 112,322 and 113,287 (§4 item 2). Id 320612 is served by the COCO host as a PNG body (HTTP 200, `image/jpeg`, 302,086 B, PNG signature) and is accepted by id only (`cen_fetch.PNG_OK`, CC-122); every other body is JPEG SOI, and the 14,500 test-side bodies had 0 failures. 112,319 records were written at `780ac71` and 320612 at the commit HEAD; `memory.done.json` carries the commit HEAD.
- **Memory record and BUILD, as run (amendment 1, 2026-10-27):** `memory.done.json` recorded 112,320, refused 2, `record_sha256` `553fb604…`, head `30514a7b…`, 2026-10-27T00:42:35Z. Within the memory, distinct sha256 = 112,308 of 112,320: 11 repeated hashes (ten pairs and one triple), joined by the byte-identical clause of C's clustering rule (§4 step 5). BUILD (`cen_memory.json` `b77e4bde…`, `cen_memory_emb.npz` `add1d92a…`, `SHA256SUMS_build` mirrored): unreadable 0; near-duplicate drops against Karpathy test 28, NoCaps val 15, Karpathy val 23 (65 distinct); kept 112,255; clusters 111,927 (111,616 singletons, 294 pairs, 17 triples). Reported beside 112,322 and 113,287.
- Data statement (CC-113 W9, CC-120 N5): COCO annotations and captions CC BY 4.0; COCO images under per-image Flickr licences (memory: ids 1–3 NC variants 77,383 of 112,322; 4 BY 18,474; 5 BY-SA 10,358; 6 BY-ND 5,650; 7 no known restrictions 457; `lists_record_coco.json`); NoCaps val images under the per-image licences listed by Open Images; NoCaps annotations under their own licence; research use; images and embeddings never redistributed.
- Transport (CC-120 W3): COCO images come over http (the coco_url as released); integrity rests on the per-file sha256 records, the JPEG-SOI and status/redirect checks of `cen_fetch.get`, and the staged re-fetch at the recorded sha.
- No caption file other than the block's reference subset and the memory caption store reaches M3; the caption store and reference subsets are built on the laptop (`cen_memory.py`), sha-recorded at staging, and deleted with the block.

## 12. What the author saw (CC-111 W8/W9, CC-115 W6, CC-107 r6, CP-116 W2)

1. **CEN anchors:** `manuscript/ken/CEN_ANCHORS_2026-10-26_v3.md` sha256 `7d0fff656ef021118175cab3dd1cdb580436613a9bb58e1279f01957454cde0f`, read as published-anchor context only; it is never a threshold source and no rows are added after this pin.
2. **163 refused-image gold exposure:** Ken's KVS precheck read Vietnamese references and COCO-English references (via uitviic_en), as aggregate verb statistics, of UIT-ViIC train images refused for dev use: 133 coco_karpathy_test, 59 coco2500, 14 chair500 and 21 pope500. These parts overlap (133 + 59 + 14 + 21 = 227 > 163 distinct images). Gold only, no model outputs. No image is dropped.
3. **Earlier outputs and gold on the C-EN sets (CC-121 r4, W3).**
   - (a) **Paper A, Karpathy test 5,000:** A scored 9 systems on the full 5,000 (r4, commit `51ef280`), including the 10-26 M3 top-up (fuse2_s42 and p1_s43 on rest2500) and the M3 reboot about 13:15Z. A's systems are Qwen2.5-VL-7B variants (C's Qwen backbone); A's zeroshot-short uses `PROMPTS["short"]`, C's Vietnamese zs prompt. All are Vietnamese; none is ret or rand, and none is reused. A used the references of 2,441 of the images (COCO-2500). The group's earlier Vietnamese VSPS zero-shot and distill decodes of all 5,000 sit in `data/results/coco5000` and are not reused.
   - (b) **A-N2 English zero-shot on 295 primary images:** A-N2 (`data/results/a_n2/a_n2_run.json`) decoded Qwen2.5-VL-7B and InternVL3-8B zero-shot with `short_en` (60 tokens, greedy, the `lb.make_generate` harness that `cen_decode.py` reuses) on CV295, which is 295 of the 5,000 primary images, and also on uv231en; G2-B did the same with Qwen3-VL. The author saw object P/R/F1 only, never CIDEr. These are the C-EN zs arm on 295 images.
   - (c) `39_y_coco_zeroshot` was dropped by D10 on 2026-10-13T01:58:50 (`queue.log` l.60) and never ran; 53_a/53_b never ran; no coco_en predictions exist.
   - (d) The English human-ceiling gold statistics on the 2,441 COCO-2500 images (R5_02) were seen. Gold only.
   - (e) No ret, rand or retrieval-ICL English output of C's backbones exists on any C-EN set.
   - No design change follows: the zs arm is descriptive and the registered rule is ret minus rand (CC-107 r5).
4. **NoCaps val:** vg-mamf's R11 decoded and scored Qwen arms on a stratified 1,000 (seed 47); reported with and without them (§3.2).
5. **C's Vietnamese verdicts were known when this file was written.** The C-EN commitment was recorded in the project's working log at 03:11:52Z and approved by the PI at 03:15:33Z (decision log PI-1026b); neither is a git commit, and the working log is not under version control; both were written after C's OpenViIC test block had started (02:18:56Z) and before the first decision file (decide_ov.json, 06:55:27Z) (CP-116 W2, PI-1026n). This prereg itself was drafted after all three C decide files existed and after the author read their headline numbers (CP-116). Its design is CC-107 r5's, fixed before any verdict.
6. Karpathy val features are used only to protect it (§3.3); no C or C-EN model output exists on it; Paper A's POPE-500 and CHAIR-500 sets include 130 Karpathy-val ids (exclusion.json, CC-106), whose A outputs are not reused or scored here.
7. **Memory fetch:** for the memory fetch the author saw only counts, bytes and progress lines, and opened no image (CC-121 W2); for id 320612 the author saw the HTTP headers and the first 8 bytes only (CC-122 X2).

## 13. Code (scripts/c_en/)

| file | sha256 | role | where |
|---|---|---|---|
| `cen_fetch.py` | `e51918e9…` (CC-120, CC-121 W2/W9, CC-122 X1, amendment 1) | lists (`lists`, `nocaps-list`), hash-only fetch, memory fetch with the W4 refusal, `--stage` | laptop / M3 |
| `cen_pool.py` | `79a45b2b…` | `embed` (SigLIP2, rate guard), `feats` (pHash/dHash/SSCD via `build_memory.features`) | M3 |
| `cen_memory.py` | `4be41c18…` (amendment 1) | `build` (§4), `exemplars` (incl. smoke), `store` (caption store, reference subsets; laptop only) | M3 / laptop |
| `cen_decode.py` | `777a5af0…` | grid, English prompts, `decode`, English guard `items`, `verify` | M3 |
| `cen_score.py` | `68a700ab…` | `score` (PTB CIDEr-D per image, guard variants), `decide` (§7) | M3 |
| `cen_job.sh` | `167a84ce…` | M3 blocks pool, feats, build, smoke, coco, nocaps; caps per family, heartbeat, attempts, machine, HEAD, venv-freeze and prereg-committed checks | M3 |
| `cen_chain.sh` | `5465e3e5…` (amendment 1) | laptop chain: hash, memory, the blocks, store/upload, `--stage`, mirror, sha-confirm, delete, cleanup | laptop |

**Amendment 1 (2026-10-27; PREREG §13; CC-124 r3 lock check).** After the BUILD block had finished and been mirrored, the laptop-side `cen_memory.py store memory` never ran: its guard `Path("/root/.vsps_machine_id").exists()` raised `PermissionError` on the laptop, where `/root` is not traversable. No file was edited before this amendment. Three changes, nothing else: (1) `cen_memory.py` `gpu_host()`: the env check first, then the machine-id file, with a `PermissionError`/`OSError` on the path counted as "not a GPU host"; new selftest cases: a raising path and a missing path are not a host, a readable machine-id file is a host, and store passes the guard to its first input (a missing NoCaps captions path, so the test reads no dataset on either machine); the `VSPS_MACHINE_ID` refusal was already tested. New sha `4be41c18…` (was `cdef2fa9…`). (2) `cen_chain.sh` step `store`: the laptop-side caption store and upload alone, refused unless `SHA256SUMS_build` is mirrored and verifies and no `cen_store` exists on M3; the store step also refuses while any tmux session runs on M3 (CC-127 W1), and refuses once `operator.log` records the store; the `build` step is unchanged. New sha `5465e3e5…` (was `38e3774b…`). (3) `cen_fetch.py` `no_pilot()`: `--stage` refuses while `/root/outputs/grl_pilot/RUNNING` exists (CC-124 r3), non-raising on the laptop, with a selftest. New sha `e51918e9…` (was `7e3cfda8…`). Disclosure: the pool, feats and build blocks ran at the pre-amendment code (`scripts/c_en/SHA256SUMS` `9f9b03c4…`; `code_at_start_{pool,feats,build}.sha256` identical) and their outputs are unchanged; no decode, score or test-set staging had run. Smoke, coco and nocaps run at the amended code; their `code_at_start_*.sha256` records list the new scripts SUMS (`9ab5fc72…`). `cen_pool.py`, `cen_decode.py`, `cen_score.py` and `cen_job.sh` are unchanged.

Full shas in `scripts/c_en/SHA256SUMS`. Reused unchanged: `scripts/c_stage1/build_memory.py` (`near`, `clusters`, `exemplars`, `features`), `guard.py` (`hf_verifier`, `fill`, `answer_position_check`), `decode_icl.py` (`exemplar_ids`, `registration`), `scripts/c_stage2/stage2.py` (`frozen`, `spec`), `scripts/lb/decode_hf_vlm.py`, `scripts/score_coco_probe.py` (`en_classes`, `load_synonyms`).

Every module has a `--selftest` on synthetic data only: it opens no test image and reads no test caption. `bash scripts/c_en/cen_job.sh --selftest` runs them all under `pipefail`: any failing module fails it, and the scorer's PTB/CIDEr-D check fails rather than skips where pycocoevalcap is missing (CC-121 W1). The gatekeeper runs it with `SCPY` on the pinned wheel `083ed791…`.

## 14. Deviations from earlier rulings (recorded, not silent)

1. **Dates.** CC-107 order items 4–5, CC-115 W9 and CC-118 W6 placed the prereg after 11-10 and the test after 11-30. PI-1026r lifts these: C-EN prereg and test this week on M3; PI-1026s: date-only gates do not bind work start. Prereg-before-decode and one look per set are unchanged.
2. **Machine.** CEN-M4-POOL is CEN-M3-POOL (CC-115 W4). The CC-113 W7 cross-machine parity gate is moot because the pool is built on the test machine; the env pin is kept (`venv-lb` `685ffe2a…` for SigLIP2, its freeze recorded in every vector file's meta).
3. **Test-side hashing is hash-only** (bytes never written) rather than a stored download, so no test image sits on M3 before its block (PT binding 3; PI-1026r(2)).
4. **NoCaps image source** is the Open Images validation bucket, not the dead NoCaps `coco_url` (§3.2).
5. **Download before this prereg's commit.** The hash-only test-side pass runs before the commit (CC-120 r2: it stores no image, decodes nothing, yields no outcome). PI-1026t: "prereg before data" means outcome data only, so the memory fetch may start once the three test-side records are complete (it overrides CC-120 r3). `--stage` of a test set waits for this commit (CC-120 r4), one block at a time, and no G-RL or CC-119 pilot runs on M3 while any `cen_<test-set>/images` exists.

## 15. Open questions for the judge

- All ruled by CC-121: Q1 English guard port with the W6 disclosure and the phrase map unchanged (r6); Q3 venv-cenfeat from the committed freeze (r7, W8); Q4 first 5 references, disclosed (r8); Q5 PTB tokens (r9); Q6 CC-107 r5's single rule, disclosed (r5); Q9 no CPU cap stop, cleanup and a judge gate (r10, W5).
- (Ruled: NoCaps source CC-120 r6; the 11.9 MB memory TSV is committed CC-120 r7; Karpathy val hash-only CC-120 r8; memory byte-duplicates refused and reported as N = 112,322 − r beside 112,322 and 113,287 with r and the matched set named, CC-120 r9; downloads PI-1026t.)
