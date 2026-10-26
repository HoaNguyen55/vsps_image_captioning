# DrivingVQA feasibility pilot note (v4): P1, P2 and P3 on all 3,142 train ids

**EXPLORATORY. Not confirmatory.** This note changes only the evaluation set and the GPU caps of v3 (`manuscript/ken/PILOT_NOTE_DRIVINGVQA_P1_P2_P3_2026-10-26_v3.md`, sha256 `d15f3e56a535e7db23e0b4e7a2b6c02951d8111eee6d6de3545c7fb76095ce16`; code `manuscript/ken/ken_dvqa_pilot_v3/SHA256SUMS` `5b2be46a795b130b159bb4f367b767dbfa931eb631e030ce00f291a5e4ceadea`). v3, v2 and v1 stay untouched. Every binding of `.session_backup/2026-10-13/decisions/CC-104.txt` (F1–F12), `.session_backup/2026-10-13/decisions/CC-104a.txt` (W1–W11) and `.session_backup/2026-10-13/decisions/CC-104b.txt` still applies, except the set size, the caps and CC-104a W12's hold-out bank (§1). Times are UTC.

## 1. What changed and why
- **PI directive, 2026-10-26** (`manuscript/WORKFLOW_LOG.md`, l.1605): train, validation and test use full datasets. No subset is sized by budget.
- **Panel CC-108** (`.session_backup/2026-10-13/decisions/CC-108.txt`, W8 and Q1) found that dev500 and dev1000 were sized for a GPU budget. It barred any run on them.
- **PI decision PI-1026c** (`manuscript/WORKFLOW_LOG.md`, l.1621–1630): "Chạy full ngay" (run full now). P1, P2 and P3 run on **all 3,142 DrivingVQA train ids**, exploratory, on M4, with a total cap of 12.6 GPU-h.
  - This supersedes CC-108's "run after 11-10" timing.
  - It also supersedes **CC-104a W12's 2,142-id confirmatory bank** (the train ids outside dev1000). That bank is now evaluated, so it is used up.
- **Consequences, stated once:**
  - No confirmatory DrivingVQA claim can be made later from train.
  - The official DrivingVQA test split stays banned. It was seen on 10-25/26 (CC-104a ruling 7, W12).
  - DrivingVQA has no confirmatory path left. Every v4 result is exploratory only. A GO authorises only a design discussion after Paper B is submitted, not before 2027-01-25 (CC-104 F9).
- **Power at n = 3,142 replaces the dev1000 power** of CC-104 F4. It is planning arithmetic with no data: a normal approximation, half-width = 100 · 1.96 · √(d/n). The source is `manuscript/ken/dvqa_train3142_power_v4.json`, written by `manuscript/ken/ken_dvqa_pilot_v4/build_splits_and_stats.py --write-power`.

  | n | 95% CI half-width per backbone, d = 15% / 25% | pooled, independent backbones | P(P1 passes ≥ 3.0) if the true gain is +3.3, pooled independent / correlated |
  |---|---|---|---|
  | 1,000 (v3) | 2.40 / 3.10 (`table.n1000.d15/d25.ci_half_width_per_backbone`) | 1.70 / 2.19 | 0.635 / 0.597 at d = 15% |
  | 3,142 (v4) | 1.35 / 1.75 (`table.n3142.d15/d25.ci_half_width_per_backbone`) | 0.96 / 1.24 (`…ci_half_width_pooled_independent`) | 0.730 / 0.668 at d = 15%; 0.683 / 0.632 at d = 25% (`table.n3142.*.p_pass_p1_true_3p3_*`) |

  - P1's point threshold (≥ 3.0) sits just below the +3.3 anchor. Even the full set therefore passes a true +3.3 only about two times in three.
  - P3's per-backbone SESOI of 10 is far outside the n = 3,142 half-width.

## 2. Sets
- **Official splits.** DrivingVQA has train 3,142 and test 789 (= 3,932 central-directory entries − 3,142 − 1 directory entry), and no official val. The test split is barred (CC-104a ruling 7, W12) and is never staged on M4. The full train split is the zero-shot dev set (CC-108 W9.1, W9.4). The 8,179 forbidden hashes in `host_check.py` are the group's own test images, not DrivingVQA's. Isolation from DrivingVQA test rests on by-name Range fetches from **train.json**, no **test.json**, the stray-image scan, and `HF_HUB_OFFLINE=1` (`job.sh:19`).
- **Source.** EPFL-DrivingVQA **train.json**, revision `02ce870cfe037b93cc034034cd747a7eecdd455c`, sha256 `4a204e3fa7516db313ceeb91ac989919979e31da20e484bc5f4018c261bd483d`, 3,142 items with 3,142 distinct `img_filename`. It is fetched by `hf_hub_download(filename=train.json)` only. **test.json** is never downloaded, opened or listed; every id comes from **train.json** keys.
- **Id list.** `manuscript/ken/drivingvqa_train3142_ids.tsv`, sha256 `39219d099ea25ccb79ce7bae13aa61b7198b9409bd468a6075b2e0b4809afc45`.
  - It holds all 3,142 train ids, ordered by `int(sample_id)`, with the same 6 columns as dev1000.
  - It is written by `manuscript/ken/ken_dvqa_pilot_v4/build_splits_and_stats.py --write-train3142`. `--selftest` checks the pin, 3,142 unique ids in int order, and dev1000 ⊂ train3142. It also regenerates the list byte for byte from **train.json** when that file is readable.
  - All 1,000 dev1000 rows are byte-identical in it.
  - There is no remainder and no exclusion.
- **Gold boxes.** 3,050 items have K ≥ 1 gold boxes and 92 have K = 0, with 4,506 boxes in total (`manuscript/ken/dvqa_train_descriptive_stats_v2.json :: subsets.train_all_3142`).
- **Image manifest.** `manuscript/ken/dvqa_train3142_image_sha256.tsv`, sha256 `7734bb326ece11cc423865ea6e83ff37986daf6fdb467ab4ea181bfcc1970708`.
  - Each row is `img_filename<TAB>sha256`, for 3,142 rows sorted by name.
  - There are 3,133 distinct SHA-256s (9 upstream pairs are byte-identical: images 0026/0533, 0073/0168, 1012/1013, 2149/2356, 2606/2685, 2754/2776, 2786/2851, 3255/3536 and 3940/4539. Each pair belongs to different items, so nothing is excluded).
  - 0 rows match any of the 8,179 forbidden test hashes.
  - Its 1,000 dev1000 rows are byte-identical to `manuscript/ken/dvqa_dev1000_image_sha256.tsv` (`ddc41513f02d5171fedc1a86146f9c708f87e09d7e88ddde83434bb7f1ef3289`).
- **Unchanged.** dev500, dev500b, dev1000 and their manifest stay committed as record. No v4 step reads them except the subset and cross-checks above.

## 3. Unchanged: prompts, parser, metrics and rules
- **Prompts.** `manuscript/ken/ken_dvqa_pilot_v4/prompts.json` is byte-identical to v3 (`712d9a3a427d5b5797e03db8695c6fe531273b799862df9bcd6455b3605841cf`). The QA prompt uses `max_new_tokens` = 16, the caption prompt 60, and step 2 is text-only.
- **Models.** The model pins (Qwen2.5-VL-7B-Instruct @ `cc594898…`, InternVL3-8B-hf @ `259a3b64…`, venv-lb `685ffe2a…`) are unchanged, and so is the training-exposure disclosure (v3 §1).
- **Parser.** `parse_answer_output` is byte-identical to v3 (CC-104a W1 grammar, v3 §2). Two record notes:
  - **Reason strings (CC-104b ruling 3 and R5).** score.py's strings are authoritative: `empty_output`, `missing_answer_header`, `empty_after_header`, `no_leading_option_list`, `ambiguous_or_between_letters`, `period_between_letters`, `trailing_standalone_option_token`, `option_out_of_range` and `missing_prediction`. v3's list of 10 names was wrong, and the mapping is in CC-104b ruling 3.
  - **Duplicates.** A separated duplicate such as `'A, A'` collapses to `[A]`.
- **Rules.** Every decision rule, SESOI and stop rule is unchanged in logic (v3 §4):
  - P1 shortcut STOP at ≤ 5.0, pooled or on either backbone;
  - P1 GO when the pooled oracle − full gain is ≥ 3.0 with LB > 0;
  - P2 GO when att − grid has LB > 0 and recovery is ≥ 0.50;
  - P3 GO when full − selfcap is ≥ 10.0 with LB > 0 on both backbones;
  - JOB STOP above 10% unparseable or above 20% empty captions.

  All comparisons use unrounded values.
- **Changed only in n.**
  - P1, P2 and P3 all score the same 3,142 items. P3 compares P3-SelfCap against P1-Full on all 3,142 items; v3 used P1-Full's dev500 rows, and v4 drops that slice.
  - There is one bootstrap index matrix, (10000, 3142), from `np.random.default_rng(0)`, sha256 of its bytes `14c037408bf79707cb165e2e74a75393c8e96d6cfc72a868bfeef6b37ecee8e6` (printed by `manuscript/ken/ken_dvqa_pilot_v4/score.py --selftest :: bootstrap_10000x3142_sha256`).
  - The descriptive K ≥ 1 check uses its own (10000, 3050) matrix and decides nothing.

## 4. Budget (CC-104 F3 rates, scaled to n = 3,142; hard caps in `manuscript/ken/ken_dvqa_pilot_v4/job.sh`)
| Step | CC-104 F3 estimate | Estimate at n = 3,142 | Cap | Margin |
|---|---|---|---|---|
| P1 (3 arms × 2 backbones) | 0.9 GPU-h at n = 1,000 | 2.83 GPU-h | 14,040 s = 3.90 GPU-h | +38% |
| P3 (caption + text QA × 2) | 0.6 GPU-h at n = 500 | 3.77 GPU-h | 17,100 s = 4.75 GPU-h | +26% |
| P2 (only if P1 GO) | 1.0 GPU-h at n = 1,000 | 3.14 GPU-h | 14,220 s = 3.95 GPU-h | +26% |
| **Total** | | 9.74 GPU-h | **45,360 s = 12.6 GPU-h** | |

- Each cap has at least 25% margin, and the total equals the PI's 12.6 GPU-h. A cap stop gives INCOMPLETE with no verdict.
- GPU-s are logged per step in the run-time file gpu_seconds.tsv (written on M4 by job.sh).
- CC-108 W8's split (P1 3.9 / P3 4.7 / P2 3.9) sums to 12.5 GPU-h, not 12.6; v4's 14,040 / 17,100 / 14,220 s = 45,360 s = 12.6 GPU-h corrects it. The split is not used, because two of its caps fall below 25%: P2 3.9 / 3.142 = +24.1% and P3 4.7 / 3.770 = +24.7%.

## 5. Code v3 → v4 (`manuscript/ken/ken_dvqa_pilot_v4/`, SHA256SUMS `550581c2d4c78379823ee3954131c7197f3ccc5654bcd6dcd9a12e9ade0c7b7b`)
| File | Change |
|---|---|
| `manuscript/ken/ken_dvqa_pilot_v4/build_splits_and_stats.py` | Adds `train3142_ids`, `check_train3142_tsv`, `power_table`, `--write-train3142` and `--write-power`, with selftest steps 4b and 5. The dev split logic is unchanged. |
| `manuscript/ken/ken_dvqa_pilot_v4/decode.py` | P1, P2 and P3 iterate the train3142 list (pin `39219d09…`). Nothing else changes. |
| `manuscript/ken/ken_dvqa_pilot_v4/score.py` | One train3142 set and a (10000, 3142) matrix; the dev500 slice is dropped. The parser is unchanged. |
| `manuscript/ken/ken_dvqa_pilot_v4/decide.py` | n = 3,142 throughout; P3 is paired against P1-Full on all items. The synthetic selftest uses n = 3,142, and the W7 edge case is recalibrated: the raw value is asserted in [2.995, 3.0), is displayed as 3.00, and still gives STOP. |
| `manuscript/ken/ken_dvqa_pilot_v4/host_check.py` | Pins the train3142 id list, the 3 prereg files and, separately, the image manifest. It expects 3,142 images. It also applies the CC-104b ruling 5 fixes required before any reuse: (c) the git-tracked name exemption applies only under the repo base; (d) only `<repo>/.git/` is skipped, so `.git` folders elsewhere are scanned. Selftests 9b and 9c cover both. |
| `manuscript/ken/ken_dvqa_pilot_v4/stage_images.py` | Takes `--ids-tsv` and `--expected-sha-tsv`, with modes `manifest`, `range` and `verify` and an optional `--reuse-dir`. Details below the table. |
| `manuscript/ken/ken_dvqa_pilot_v4/job.sh` | Uses the train3142 image manifest and the caps in §4. Nothing else changes. |
| `manuscript/ken/ken_dvqa_pilot_v4/prompts.json` | Byte-identical. |

`manuscript/ken/ken_dvqa_pilot_v4/stage_images.py` in detail:
- `http_fetch_byte_range` is byte-identical: it requires 206 and a matching Content-Range before `read()` (W7). The per-entry 30-byte header and the exact `name+extra+comp_size` read are unchanged.
- **CC-104b (b).** The EOCD read is exactly 22 bytes. A ZIP comment, or a CD that does not end at the EOCD, is refused. The selftest asserts that no unlisted payload appears in any fetched chunk, the EOCD and CD reads included.
- Each image is checked against the CRC-32 and size in the CD and against the 8,179 forbidden hashes.
- In manifest mode, the dev1000 rows must equal `ddc41513…`.
- A reused file is taken only if its SHA-256 matches the pinned list and its CRC-32 and size match the CD.
- The unused local-zip extractor is deleted.

## 6. Staging (operator workstation, local; nothing is on M4)
- **Sequence.** Run `manuscript/ken/ken_dvqa_pilot_v4/stage_images.py --mode manifest` (laptop, venv with `huggingface_hub`). This writes the image manifest. Pin its sha in `manuscript/ken/ken_dvqa_pilot_v4/host_check.py`, then run `manuscript/ken/ken_dvqa_pilot_v4/stage_images.py --mode verify` with the final v4 code. Verify mode is offline: it re-hashes the staged folder against the pinned manifest.
- **Sequential requests.** The run makes 2 Range requests per fetched image. Bounded concurrency was not added. Sequential requests keep every request on the unchanged W7 path and avoid HF rate limits, which would fail closed with no resume.
- **Reuse.** The 1,000 dev1000 images came from the operator's earlier Range-only staging (v3 `http_range` mode, manifest `ddc41513…`), not from Ken's staging, so CC-104a W12's "reused none of Ken's staging" still holds. Each was reused only where it matched its `ddc41513…` row and its CD CRC-32 and size.
- **Result** (`.session_backup/2026-10-26/dvqa_pilot_v4_staging/stage_manifest.json`, git-excluded):
  - `extracted_count` 3,142, of which `reused_count` 1,000 and `fetched_count` 2,142;
  - `total_cd_entries_scanned` 3,932, `total_payload_bytes_fetched` 442,248,414 and `total_extracted_bytes` 664,920,195;
  - `dev1000_rows_match_ddc41513` true, `manifest_sha256` `7734bb32…`.
  - Staging ran on v4 code before the two pins were filled in (`IMAGE_SHA_TSV_PIN`, `TRAIN3142_DISTINCT_IMAGE_SHAS`). Verify mode then ran on the final v4 code (`.session_backup/2026-10-26/dvqa_pilot_v4_staging/stage_verify.json`): `verified_count` 3,142, `distinct_sha256_count` 3,133, `total_bytes` 664,920,195, `train_json_sha256` `4a204e3f…`, with 0 forbidden (verify refuses otherwise).
- **test.json.** `find` over the staging folder and the HF_HOME used for staging finds no **test.json**. The final run's temporary download folder was removed when it ended. An earlier run's folder `/tmp/dvqa_stage_sygmc82j` (created 08:43 VN) was **not** removed: it still holds **train.json** and a `.cache` folder, and no **test.json**. The operator deletes it after the M4 copy (CC-104c W4). No request named **test.json**.

## 7. Before any GPU step
1. **Code read.** One judge reads the code and this note (CC-108 W8: "a code-read round and the gatekeeper before any GPU").
2. **Gatekeeper.** Commit v4, copying **only v4** to `scripts/ken_dvqa_pilot/` in place of v3, together with the two new TSVs, the power JSON and this note. The v4 SHA256SUMS pin goes first in the commit message (CC-104b R2). The operator passes the full 64-hex pin as job.sh argument 2 (R3).
3. **Operator on M4.**
   - Run the W10 CPU host_check with an empty M4 path /root/dvqa_pilot; it must show only `missing_*`.
   - Run CC-104b R4's two commands; they must print nothing.
   - Copy the 3,142 staged images and **train.json** to the M4 path /root/dvqa_pilot, then run job.sh.
4. **Ken.** Ken has no machine access (CC-104).
5. **Writer.** v4 was written by the operator's writer, not Ken: a recorded deviation from CC-104's "Ken writes", because the PI asked to run now (PI-1026c). The panel read CC-104c is the independent check.
