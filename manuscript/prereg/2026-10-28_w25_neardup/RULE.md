# W25 near-duplicate pass: UT-2,402 against KV-5,000 and OIV7 val, before any K2 Gate 1 training

**Status:** written 2026-10-28, before any W25 output. No UT×KV or UT×OIV7 distance, count or pair has been computed, and no OIV7 val image has been fetched. The rule binds once the gatekeeper commits it with `scripts/w25/`, after a judge read (CC-151 r12). `EXPECT_HEAD` in `w25_job.sh` is that commit. v2 carries the CC-153 (I) fixes W1–W5 (panel GO-with-fixes 3/3, 2026-10-28).

**Label:** LEAKAGE EXCLUSION, training side only. It removes UT-2,402 training images; it never removes a test image. This is a principled, pre-fixed, disclosed exclusion of the kind the full-datasets rule allows (dedup / leakage).

**Sources:**
- CC-148 W9 (= CC-119 W25): a pHash/SSCD near-duplicate pass of UT-2,402 against KV-4,224 and OIV7 val, on M3, before any training; Gate 1 stays HELD until it is done.
- CC-151 r2 and r12, PI-1026bb Q2 (run order on M3: W25 → byte deletion logged → MT4 PREREG → Gate 1).
- CC-119 W25 ("C-EN's pHash/SSCD near-duplicate pass"), C-EN PREREG §2–§4, dev-pools DESIGN §5 (the registered match rule).
- Ken's K22-2 §8 (draft; its pHash ≤ 8 has no source and is not adopted).

## 1. Sets

| Set | Size | Features | Bytes fetched by W25 |
|---|---|---|---|
| UT-2,402 (`ut2402.txt`, sha 3969bfd4) | 2,402 | computed by W25 from the images already staged on M3 (`uitviic/images`, checked against `images.sha256`) | none (train side, already staged) |
| **KV-5,000** (`kv5000.txt`, sha b7a7a89d) | 5,000 | **C-EN's** `feats_coco_kval.npz` (sha 9783f7a6…, 0 unreadable, C-EN SHA256SUMS_feats, head 30514a7b, 2026-10-27) | **none** |
| OIV7 val (`oiv7_val_ids.txt`, sha 4b7a1813, this folder) | 41,620 listed; **41,164 compared** | NoCaps val 4,500 (all in OIV7 val) minus its 43 XM3600 images: C-EN's `feats_nocaps_val.npz` (sha b69dac29…), 4,457 rows; the other 36,707: computed by W25 | the 36,707 only, under §5 |

- **The 456 XM3600 ids (CC-153 r4).** OIV7 val compared = 41,164 (41,620 − 456 XM3600, refused for every non-C use; protects C's XM-test2500 one-look, C test PREREG l.14). The 456 ids are `xm3600_in_oiv7_val_ids.txt` (this folder, sha 54966ca7), made once on the laptop as the `id`s of XM3600 `full_data.json` (sha 101d24ad, ids only read) that are in `oiv7_val_ids.txt`; `full_data.json` is never on M3. They are dropped by id before any fetch: 413 are never fetched and the 43 NoCaps val rows are dropped from C-EN's existing features, so no XM3600 byte reaches tmpfs and no new XM3600 feature row is made. Backstop: a fetched body whose sha256 is in `exclusion.json` `image_sha256.xm3600_all_images` is never written and is a FAULT.
- **KV-5,000 instead of KV-4,224 (erratum, CC-153 r5).** The KV-4,224 list is already pinned (`id_counts.json` `kv_pool_a_excluded` = 4,224, sha 86d93863…); v1 wrongly said it was not. KV-5,000 is kept as the superset by choice: it reuses C-EN's `feats_coco_kval.npz` (9783f7a6) with no new KV byte, and comparing against a superset can only exclude more training images, never fewer. W25 is not rerun for the 4,224 list.
- **OIV7 val list.** The 41,620 `ImageID`s of the official `validation-images-with-rotation.csv` (Open Images, 2018_04 release; V7 keeps the same validation images). The file's md5 equals the storage bucket's `x-goog-hash` md5 (`ZDpU5DsLq4rM6IF7SlaXgA==`, 15,245,485 bytes, checked 2026-10-28). Only the ids are committed; the CSV is not.
- Image URLs come from `cen_fetch.OI_URL` and `cen_fetch.get` (no redirect, status 200, JPEG body), the C-EN NoCaps fetch path accepted by CC-120 r6. No new host appears in this rule or its code.

## 2. Features (unchanged code)

- Every feature is `build_memory.features` (C stage-1, unchanged), which calls `match_openviic._features` / `_mirror_hashes`: imagehash 4.3.2 pHash and dHash (64 bit) on the EXIF-oriented RGB image, the same two hashes of the mirrored image, the SSCD `sscd_disc_mixup` TorchScript descriptor (sha 9f26bd4c, the C-EN weights) with `small_288` preprocessing, and the file sha256.
- This is the exact code that produced C-EN's KV and NoCaps features, so all sides are comparable.
- venv: `venv-cenfeat` on M3 (freeze 1a639a50, CPU torch, C-EN PREREG §2). No GPU is used.

## 3. The rule (fixed now)

A UT image is **excluded** if, for at least one image of KV-5,000 or of OIV7 val:

| | Criterion | Source |
|---|---|---|
| C1 | byte-identical (equal sha256) | — |
| C2 | min(pHash, dHash) ≤ 10, with UT's mirrored hashes, **and** SSCD cosine ≥ 0.5 | the group's registered match rule (dev-pools DESIGN §5; `match_openviic.is_match`; `build_memory.near`, the rule C-EN already applied to these KV features). The 0.5 floor is the level Somepalli et al. (CVPR 2023, arXiv 2212.03860, §7) use for "very close matches (> .5 SSCD)" |
| C3 | SSCD cosine **> 0.75** | the SSCD authors' calibration: "For the `sscd_disc_mixup` model, DISC image pairs with embedding cosine similarity greater than `0.75` are copies with 90% precision" (facebookresearch/sscd-copy-detection README; Pizzi et al., CVPR 2022, arXiv 2202.10261) |

**Excluded = C1 ∨ C2 ∨ C3.** C1 ∨ C2 is `build_memory.near` called unchanged; C3 is `w25.sscd_any`.

**Why a union.** Missing a leaked image costs a contaminated test claim; excluding a clean training image costs one of 2,402 examples. The union favours recall. C3 is the only criterion with an externally calibrated precision; C2 is the group's existing rule, kept so W25 is the same pass CC-119 W25 names.

**Not adopted.** Ken's pHash ≤ 8 on its own: no source. A hash-only criterion is never used; the hashes only propose, SSCD confirms (C2).

**Reported, never excluding:** the count at SSCD ≥ 0.5 alone (Somepalli's level) per set, as a sensitivity line.

**Lost images.** An OIV7 image that cannot be fetched after `cen_fetch.get`'s three tries, or cannot be decoded, is not compared and is counted. More than 41 (0.1% of OIV7 val) lost is a FAULT → TO-PI. KV and UT must have 0 lost (FAULT otherwise).

**No visual check.** No one looks at any pair. Looking would be new labelling.

## 4. Steps (`scripts/w25/w25_job.sh`, M3, tmux, CPU)

0. Import check first (`w25.py imports`, exit 3 = FAULT); the job selftest (`w25.py --selftest`, `bash -n`, SHA256SUMS, no `| tee`, GPU=m4 refused); the venv-cenfeat freeze and `pip check`; the SSCD weights sha (9f26bd4c); `w25.py preflight` (CC-153 W2: `feats_coco_kval.npz` 9783f7a6 and `feats_nocaps_val.npz` b69dac29 at their shas, KV ids = `kv5000.txt`, every NoCaps id mapped to its OIV7 id, 41,164 to compare); then **`common.guard` verbatim** and no `/dev/shm/w25` (`w25.py guard`). Any mismatch is a FAULT before any fetch.
1. `feats-ut`: the 2,402 staged UT images, written by tmp + rename.
2. `feats-oiv7`: the 36,707 OIV7 val images outside NoCaps val and XM3600, in batches of 512 (§5). One part file per batch; a rerun skips finished parts.
3. No `scripts/w25/w25.py` process left (`pgrep -f 'scripts/w25/w25[.]py'` empty; the plain `scripts/w25/` pattern would match the job itself); `/dev/shm/w25` must be gone; **`common.guard` verbatim** again; one `runs.log` line records it.
4. `decide` (CPU, one look): `w25_excluded_ids.txt` (sorted UT ids, possibly empty) and `w25_decide.json` (counts per criterion and set, excluded by both sets, lost images and their OIV7 ids, input shas). Then the outputs' `SHA256SUMS`.

**Job hygiene.** `set -euo pipefail`; every command writes `>> log 2>&1`, never `| tee`; lock `/root/outputs/w25/RUNNING` (noclobber) with no other `/root/outputs/*/RUNNING`; exactly one tmux session; committed clean HEAD; host id `m3`.

**Cap.** One wall cap of **3.25 h** for steps 1–2 (the W25 reserve inside dev 40, CC-151 r6, PI-1026bb Q3). The deadline is fixed at the first start and kept across reruns. Exit 124 is NOT-RUN (cost) → TO-PI, and K2 Gate 1 stays HELD; it is never a reason to relax §3. A fault writes `W25_FAULT_<utc>.txt`; a logged rerun is allowed while `w25_decide.json` does not exist.

## 5. Byte handling and the M3 guard amendment

**KV.** W25 fetches **no** Karpathy val byte. C-EN staged Karpathy val once, feature-extracted it and deleted it (`deletions.log`: "2026-10-27T03:00:12Z deleted /root/ncs-data/datasets/cen_coco_kval after its features"). W25 reads only those features.

**OIV7 val.** The 36,707 images are fetched to M3 only, one batch of ≤ 512 at a time, into `/dev/shm/w25/b<NNNN>/` (tmpfs, RAM). The batch is unlinked as soon as its features exist. Each deletion is logged in `/root/outputs/w25/deletions.log` (utc, folder, file count). On any job exit the trap deletes `/dev/shm/w25` and logs that too. The 456 XM3600 images of OIV7 val are not among them: they are dropped by id before any fetch (§1, CC-153 r4).

**What leaves M3 (CC-153 W5).** `feats_ut.npz` and `oiv7_parts/` are never committed and are read only by `decide`. Only `w25_excluded_ids.txt` and `w25_decide.json` leave M3, and only through the gatekeeper (§7).

**Amendment to the M3 isolation (PILOT_RULE §7 / `common.guard`), W25 job only.** Minimal and explicit; `scripts/grl/common.py` is not changed.
> (a) `common.guard` runs verbatim before the first W25 step and after the last. (b) Between them, and only inside the W25 job holding its lock, OIV7 val image bytes (never an XM3600 image) may exist on M3, only under `/dev/shm/w25` (tmpfs, outside `common.SCAN_ROOTS`), at most one batch of 512 at a time; each batch is deleted right after its features and the deletion is logged. (c) No Karpathy val byte is fetched. (d) No GPU is used and no other job runs. (e) The K2 Gate 1 job refuses to start while `/dev/shm/w25` exists.

Why this is needed: `common.scan` refuses any image whose name is not a COCO file name, so an OIV7 file under a scan root would make every later guard refuse; and the guard's purpose (no test image on disk when a model runs) is kept by (a), (b) and (e).

## 6. Are SSCD descriptors a "model output on Karpathy val"? (for the judge)

PILOT_RULE l.37 keeps the 130 Karpathy-val ids out of the Gate-1 pool "so that no model output ever exists on Karpathy val", citing C-EN PREREG l.67/l.159 as its source.

**Writer's position: no, and in any case W25 creates none on KV.**
1. **W25 computes nothing on KV.** It reads C-EN's existing KV features. Whatever their status, W25 adds no new descriptor of any KV image.
2. **The rule's own source treats them as allowed.** C-EN PREREG §3.3 (l.69), the document PILOT_RULE l.37 cites, says of Karpathy val: "It is hashed and feature-extracted for the memory-side near-duplicate pass only, then deleted; no model output is ever produced on it." The same sentence that bans model outputs on KV registers SSCD feature extraction on KV. So under the registered reading, a copy-detection descriptor is not a "model output".
3. **Purpose.** The ban protects KV as a one-look test: no caption, prediction or score of any system may exist before the MT4 scoring event. A copy descriptor is not a caption, cannot be scored by any MT4 metric, carries no information about any MT4 system, and is used only to delete training images.
4. **Counter-argument, stated fairly.** SSCD is a trained ResNet50, so its descriptor is literally the output of a model. A strict reading would ban it. Under that reading C-EN's KV features were already a breach, and W25 cannot undo it; W25 would then have to drop KV from the pass and keep OIV7 val only, leaving CC-148 W9's KV check undone.

OIV7 val is the G1′ fallback test set (PI-1026u Q7), not Karpathy val; PILOT_RULE l.37 does not name it. W25's OIV7 descriptors are produced under §5 and used only for this exclusion.

**Ruled (CC-153 r1, 3/3).** An SSCD descriptor, perceptual hash or sha256 is not a "model output" under PILOT_RULE l.37; the term means a caption, prediction or score of any evaluated system. W25 produces no caption, prediction or score of any evaluated system, on KV or on OIV7 val. KV stays in the pass.

## 7. Hand-off to K2 Gate 1

- The gatekeeper copies `/root/outputs/w25/w25_excluded_ids.txt` (byte for byte, sha checked against the W25 `SHA256SUMS`) to `manuscript/prereg/2026-10-28_k2_gate1/w25_excluded_ids.txt` as K2 Gate 1 amendment 1, adds its sha to that rule's `SHA256SUMS`, and commits it with `w25_decide.json` beside it.
- Before the K2 Gate 1 job: `deletions.log` and the post-run guard line are mirrored and logged in WORKFLOW_LOG (the "byte deletion logged" step of the CC-151 run order).
- Gate 1 reports 2,402, 2,532 and 2,695 beside the post-W25 pool.

## 8. Disclosures (pre-written)

- "Training images that were byte-identical or near-duplicates of any Karpathy val (5,000) or Open Images V7 validation image (41,164 compared: 41,620 − 456 XM3600 images, which are refused for every use outside Paper C) were removed before training (n = N of 2,402). A pair counted as a near-duplicate if its SSCD copy-detection cosine exceeded 0.75 (the SSCD authors' 90%-precision operating point on DISC), or if its pHash or dHash distance was at most 10 bits with SSCD cosine at least 0.5. No pair was inspected visually."
- The thresholds were calibrated on DISC (and, for 0.5, on generated images), not on COCO or Open Images.
- The SSCD input is decoded with PIL `im.draft` (`match_openviic.load_image`: JPEG decoded at the smallest 1/2^k scale with short side ≥ 288 px) before the `small_288` resize, not with the full-resolution decode of the SSCD reference pipeline, so the DISC 0.75 calibration holds only approximately for these descriptors. The same decode produced C-EN's KV and NoCaps features, so all sides stay comparable.
- KV features were computed once by the C-EN pipeline on 2026-10-27 and reused.

## 9. Judge items

- **W1.** §6: are SSCD descriptors on KV a "model output" under PILOT_RULE l.37? If yes, KV is dropped from the pass (§6 point 4), and that drop goes to the PI.
- **W2.** §3: the union C1 ∨ C2 ∨ C3 (writer default), or C3 alone (sourced only), or C2 alone (the registered rule only)?
- **W3.** §5: the guard amendment. (CC-153 r3/r4: accepted; the 456 XM3600 images are dropped by id and never pass through tmpfs.)
- **W4.** §1: KV-5,000 kept as the superset of the already pinned KV-4,224 list (`id_counts.json`, sha 86d93863…), by choice, reusing C-EN's KV features.
- **W5.** §3: lost OIV7 images tolerated up to 41 (0.1%), else FAULT.
- **W6.** §4: the 3.25 h wall cap for a CPU pass of about 37k downloads and features. C-EN's measured rate was about 0.14 s/img for features (5,000 KV in about 12 min), so features alone project about 1.5 h plus 6 min for UT. Download time: the C-EN NoCaps fetch anchor (4,500 images in 7m08s, about 0.095 s/img) projects the whole pass at about 1.5–2.5 h against the 3.25 h cap.

## Amendments

(none)
