# Post hoc rows needed by the integrity audit: plan v1.1 (gate 2)

Stamp 2026-11-10T15:22Z. One-judge FULL read, REVERSIBLE tier, ≥ 85. Replaces v1 (9f7a5e74). Authority: PI-1110n (LOG:2070; it answers CC-199 Q2 and Q3). This step counted ids and pinned lists. It computed no score or result row and printed no caption, prediction or per-image score: ledgers and caption files were re-hashed only; decision files and the B2 record were read for keys, lengths and registered aggregate fields.

Paths: `RUN` = /mnt/d/vsps_image_captioning; `PA`, `PB`, `PC` = the paper repos; `M3c` = RUN/.session_backup/machines/M3/root/outputs/c_test; `M1e` = …/M1/root/outputs/c_en; `M4b` = …/M4/root/outputs/b1_scaling; `IDS` = `ids/` beside this file; `POST` = RUN/.session_backup/2026-11-10/posthoc; `SCR` = RUN/scripts/posthoc_1110; `PY` = `~/.venvs/c_stage1_lists/bin/python -I -B` (`score_t`, `cen_score`, `b1`, `a_t3` import under it). Shas are 8-hex prefixes; full lines: IDS/INPUTS.sha256 (inputs), IDS/SHA256SUMS (pins); pin commands: IDS/COMMANDS.txt. Every row runs as `PY SCR/<script> --ids <ids file> --out POST/<output>`.

## 1. Fixed rules

1. Every row is labelled POST HOC, carries no verdict and is printed beside the registered result.
2. No registered label, threshold, set or sentence changes.
3. A row is reported whatever its value; if it cannot be computed, the reason is reported.
4. Estimator, bootstrap seed and B are those of the registered analysis. Per-image scores are read unchanged; document frequencies are not recomputed.
5. The computing step reads only the inputs listed for its row, checks each sha first, runs once on the laptop CPU and writes one OPS line.
6. Each script first reproduces the registered number within 1e-9 (identity check); a failed check stops the row.
7. Order: judge read; the five scripts with synthetic selftests (gate 3), committed before any ledger is opened; each row once; result read (gate 6); each repo's diff gate.

## 2. Pinned lists (done)

**Rule**, quoted from CC-199_checks/xtab3.py:27: `(((np.minimum(ph, dh) <= BM.HASH_MAX) & (s >= BM.SSCD_MIN)) | (s > 0.75) | same)`, with `HASH_MAX, SSCD_MIN = 10, 0.5` (build_memory.py:30) and the memory image's mirrored hashes. It is C1 ∨ C2 ∨ C3 of the W25 rule (RULE.md:38-42; CC-199:28).

**Shown examples.** `exemplar_ids` (decode_icl.py:181-190) takes the first k stored ids, for `ret` and for `rand`; k is 8 for Qwen2.5-VL and 4 for InternVL3 (frozen_config.json 2f0c32be; run names at M3c/SHA256SUMS_ov:2, :3, :6, :7). Rank is retrieval rank; order `last` reverses only the prompt position. τ acts on captions after decoding and removes no example.

**Method.** IDS/pin_ids.py (2fb61436) sha-checks each CC-199 script, runs it unchanged, keeps its output, dumps ids through the script's own pair function and stops unless the dump equals the printed counts.

| Pin: set (n) | `ret`: flagged, at rank 1 | List (sha, ids) |
|---|---|---|
| PIN-C: OpenViIC test, primary (1,941) | Qwen2.5-VL, k 8: 12, 9. InternVL3, k 4: 12, 9 | pin_c_ov_test_ret_union.txt (8c75134e, 12) |
| PIN-C2: XM-test2500 (2,500) | 0 for both | pin_c2_xm_test2500_ret_union.txt (e3b0c442, empty) |
| PIN-C2: COCO Karpathy test (5,000) | 1, 1 for both (id 179441) | pin_c2_coco_test_ret_union.txt (c2b749ec, 1) |
| PIN-C2: NoCaps val (4,500) | 0 for both | pin_c2_nocaps_val_ret_union.txt (e3b0c442, empty) |
| PIN-K: KTVIC test (558) vs train (3,769) | 16; 2 byte-identical (507, 1335) | pin_k_ktvic_test.txt (a4c7d272, 16) |
| PIN-K: dev300 vs the other 3,469 | 7; 1 byte-identical (2004) | pin_k_ktvic_dev300.txt (dd284b51, 7) |

- `rand`: 0 flagged in all four sets, at k 8 and at k 4.
- PIN-C: the per-backbone lists are byte-identical. Each query has one flagged example, by the SSCD clause alone (0.750 to 0.920): 9 at rank 1, 2 at rank 2, 1 at rank 3, none at ranks 5 to 8 (pin_c_ov_test.json 4455d9f4).
- PIN-C2 controls: on the English feature files the registered rule recovers the images cen_memory.json dropped (28 COCO, 15 NoCaps); XM rows carry the listed sha256 values; 299 images in both feature runs agree exactly; no pool image exceeds SSCD 0.51 against XM-test2500 (xm_control_stdout.txt).

## 3. Rows

### C1. Paper C, OpenViIC test without the 12 queries. READY TO COMPUTE

- **Ids:** IDS/pin_c_ov_test_ret_union.txt (8c75134e), 12.
- **Inputs:** M3c/ledger_ov_test_1941.jsonl 50878193 (decide_ov.json::ledgers; SHA256SUMS_ov:14); M3c/decide_ov.json 9bcad498 (SHA256SUMS_ov:16); lists.json 5c479f03; frozen_config.json 2f0c32be; scripts/c_test/score_t.py de942942 (its SHA256SUMS:2).
- **Estimator:** P1 = per-image `cider_s`, `ret` − `rand`, at each backbone's frozen τ, averaged over the two backbones and over images; `S.boot`, B = 2,000, `default_rng(0).integers(0, n, (B, n))`, percentile 95% CI, n = 1,929 (PC/prereg/2026-10-25_c_test/PREREG.md:131; score.py:41, :246-250; decide2.py:88-103). P2 per backbone by `S.pcm_ci` on the same queries (score.py:253-259; PREREG.md:184; CC-199 W6).
- **Script, output:** new, at most 40 lines, `c1_row.py`, importing `score_t`; `c1_ov_test_posthoc.json`. `raw = aliased(S.latest(read_jsonl(ledger)), "ov_test")`. Identity: `DD.gate(reorder(raw, order), cfg, "ov_test")`, with `order = T.scored_ids("ov_test_1941", lists)`, equals decide_ov.json::P1 and ::P2. Row: `DD.gate(reorder(raw, keep, subset=True), cfg, "ov_test")`, `keep` = `order` without the 12 (asserted to lie in `order`).
- **Sentence:** FIX_C.md C-01, targets 1 to 3, with n_flag 12, n_rank1 9, n_rand 0, so "can only raise" stays.

### C2. Paper C, the other three test sets. READY TO COMPUTE

- **XM-test2500 and NoCaps val:** 0 flagged in both arms: FIX_C.md C-05's first clause with the count 0; no row.
- **COCO ids:** IDS/pin_c2_coco_test_ret_union.txt (c2b749ec), 1.
- **Inputs:** M1e/ledger_coco_test_5000.jsonl 58074dae (decide_coco_test.json::ledger_sha256; SHA256SUMS_coco:12); M1e/decide_coco_test.json efc6eac7 (SHA256SUMS_coco:13); frozen_config.json; scripts/c_en/cen_score.py 68a700ab (its SHA256SUMS:5).
- **Estimator:** pooled `ret` − `rand` in `cider_ptb`, per-image differences averaged over the two backbones; `ci(d[sel], draws(n))`, B = 2,000, `default_rng(0).integers(0, n, (B, n))`, n = 4,999 (PC/prereg/2026-10-27_c_en/PREREG.md:95; cen_score.py:31, :126-132; subset form as cen_score.py:214-228).
- **Script, output:** new, at most 30 lines, `c2_en_row.py`, importing `cen_score`; `c2_coco_posthoc.json`. Identity: `one_set(rows, "coco_test", "coco_test_5000")["pooled"]` equals decide_coco_test.json::P1_EN.
- **Sentence:** FIX_C.md C-05 with COCO n_flag 1, n_rand 0, n 4,999.

### A1. Paper A, COCO val2017 fit without InternVL3. BLOCKED

- **Blocked by a missing input and one ruling.** The test gold (144bc513, tier3.json::provenance) stayed on M1 by design (LOG:985, :1037) and M1 is deleted. Its source, the public `annotations_trainval2017.zip` (pin 113a836d, a_t3.py:70), is not on the laptop (RUN/data, RUN/.session_backup and the home folder searched; the sealed folder pruned, not opened or listed). `cmd_gold` and `instances` refuse off the m3 machine (a_t3.py:222, :168-169).
- **Needed:** (1) fetch the zip and check its pin; (2) a judge ruling that the wrapper may make `a_t3.machine_id` return "m3" in-process, editing no registered file, and call `cmd_gold` unchanged. The rebuilt file must hash to 144bc513, or the row stops.
- **Inputs confirmed:** the 8 caption files (M1 a_t3_t3/SHA256SUMS, odd lines 3 to 17; all verify); test list 5aaa479f (PA r9/SHA256SUMS:2; 3,232 ids); val2017_ids.txt ea37cee0; dataset_coco.json 2fd99922; tier3.json 5735bd20 (TIER3.sha256); a_t3.py 57507e09 (= tier3.json::provenance.script_sha256).
- **Estimator:** `a_t3.analysis` (a_t3.py:507-551). AD-1′: multinomial image weights, 1,000 draws, seed 0, percentile 95% CI (PA/prereg/2026-10-30_a_t3/PREREG.md:185; p50.py:56; a_t3.py:520). X5: 1,000 null replicates from `default_rng(0)` (PREREG.md:190; p50x.py:28; a_t3.py:544-545). Minimum 3 models (PREREG.md:178).
- **Fixed now.** `analysis` rebuilds the clean set from the runs it receives, and the one-reference draws run over the whole id list (a_t3.py:193-196; p50.py:160-165). So the wrapper never shortens that list. It calls `analysis` with the 3,232 ids and the four models in tier3.json::models order. Identity: n 3,226, AD-1′ +35.4553 [34.1871, 36.5632], X5 observed −26.7943 against null [−8.7578, −6.6911]. For each left-out model it passes the six remaining runs without the captions of the 6 registered-unclean images, and asserts the registered index array; scores and null draws read captions only at indexed images (score_g2b.py:192-197; p50x.py:94-104). Rows: without InternVL3 (primary); the three other leave-one-out fits beside it.
- **Script, output:** new, at most 60 lines, `a1_lomo.py`, with `--ann <zip>` in place of `--ids`; `a1_lomo_posthoc.json`. It never calls `cmd_score` and writes nothing under data/results/a_t3.
- **Sentence:** FIX_A.md A-04.

### B1. Paper B, development slope without the 7 images. READY TO COMPUTE

- **Ids:** IDS/pin_k_ktvic_dev300.txt (dd284b51), 7.
- **Inputs:** M4b/ledger.json 4afa3f44 (decide.json::ledger_sha256; M4b/SHA256SUMS:70); M4b/decide.json b44a76fe (SHA256SUMS:67); scripts/b1_scaling/b1.py e747205e (= decide.json::code_sha256); scripts/scaling_probe.py 0342f6e5.
- **Estimator:** the registered sensitivity formula with a set in place of one image (PB/prereg/2026-10-28_b1_scaling/PREREG.md:84, :88; b1.py:472-489). Point means over the other 293 images; index matrix `default_rng(0).integers(0, 300, (2000, 300))` (scaling_probe.py:54, :57; b1.py:431) with the draws of the 7 dropped; `fe_slope` over seeds 42, 43, 44; percentile 95% CI (`ci`).
- **Script, output:** new, at most 30 lines, `b1_mask7.py`, importing `b1`; `b1_mask7_posthoc.json`. Identity: the empty set reproduces decide.json::P-B1 (+9.6096 [7.1759, 12.3648]); image 2004 alone reproduces ::sensitivity_minus_dev_twin.pooled (+9.6078 [7.1690, 12.3700]).
- **Sentence:** FIX_B.md B-03, with 7 and 293.

### B2. Paper B, headline test mean without the 16 images. READY TO COMPUTE

- **Ids:** IDS/pin_k_ktvic_test.txt (a4c7d272), 16.
- **Inputs:** RUN/data/results/b_posthoc/b_posthoc_mbr3_run.json 7a51aadf (commit 5962420; PB/paper/number_manifest_B.tsv:640-643), keys `test_ids` (558) and `per_image_cider_x100` for s42, s43, s44: per-image word-level CIDEr of the three headline result files (ea38b60e, ce8576a4, 723d9765) on the 558-image document frequencies, unrounded and in `test_ids` order (score_b_f1.py:449, :468). Also cider_3seed_mean.json f6f68d02.
- **Estimator:** the registered headline is the mean over three seeds with the sample SD (number_manifest_B.tsv:82-83). It has no bootstrap, so none is added. Row: per seed, the mean of the stored values over the 542 kept images; then mean and sample SD.
- **Script, output:** new, at most 15 lines, `b2_mask16.py`; `b2_ktvic_test_posthoc.json`. Identity: the 558-image means equal 148.6640, 148.0630 and 147.9615. It reads no caption and no KTVIC file.
- **Sentence:** FIX_B.md B-02b with 14 and 16. Its clause "we did not re-score…" is replaced by: "Post hoc, without these 16 images the three-seed mean is [ROW-B2: mean, SD] on 542 images (no verdict; the reported 148.23 is unchanged)."

## 4. Checks for the judge

1. `sha256sum -c IDS/SHA256SUMS` passes; each IDS/INPUTS.sha256 line equals the manifest line cited here.
2. `pin_ids.py`, re-run in an empty folder, gives the same sha for every pin.
3. The kept outputs of the unchanged CC-199 scripts equal CC-199:33-38 and :81-82.
4. `pin_ids.py` flags only through `xtab3.pairhit` and `xtab2.pair`; `clause()` only annotates.
5. The shown-example definition (first k, both arms) is right, and the zero counts rest on the controls of §2.
6. Row scripts call registered code unedited.
7. A1: accept or refuse the fetch, the in-process guard override and the device that holds the 3,226 set.
8. B2 reads a committed post hoc record, not the caption files: accept or refuse.
9. Sentence templates are fixed now; outputs carry the label and input shas and stay outside prereg and registered result folders.

## 5. Changes from v1

1. PI-1110n answers the PI questions of v1 §1 item 6. B2 is now a row and needs no re-score: a committed record holds the per-image values.
2. PIN-C: xtab3.py already counts ranks 1 to 8: 12 at k 8 and at k 4, so one list replaces v1's two.
3. PIN-C2 is done (0, 1, 0), so C2 is one COCO row. No needed file is sealed or missing.
4. A1 moved to BLOCKED: v1's "registered gold step" cannot run off m3, and a three-model call as v1 wrote it could change n.
5. CC-199:91 called the 12 an upper bound because of τ. τ filters captions, not examples, so 12 is exact.
6. M1 a_t3_t3/SHA256SUMS:1 (EVENTS, a log) no longer verifies; it is not an input.
