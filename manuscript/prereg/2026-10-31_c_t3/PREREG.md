# C-T3: tier-3 TEST prereg for Paper C (Flickr30K Karpathy test, 1,000 images, one look; the three E3 claims)

Status: Committed deee879; amended by <this commit> (Codex W5 read fixes #2-#6, wording for #1). Written 2026-10-31
after the tier-2 decision and before any test byte was extracted. Nothing here has run. This is AI opinion, not expert-validated. Label on every output: `TIER 3 / TEST, ONE LOOK
(C-T3)`. Launch read: irreversible tier (the run spends Flickr30K test's single look), bar ≥ 92 (band 92-98,
PI-1029o), 3-judge panel + Codex (JUDGE_READ_REQUEST.md).
Code: `scripts/c_t3/c_t3.py` (a copy of `scripts/c_t2/c_t2.py` sha256 `6113844a` with the smallest change; read it as
`diff scripts/c_t2/c_t2.py scripts/c_t3/c_t3.py`), `scripts/c_t3/c_t3_job.sh` (from `c_t2_job.sh` `17ad5227`),
`scripts/c_t3/c_t3_neardup.py` (new, about 150 lines; it imports the W25 rule unchanged). Tier-1/2 files are not edited.
Tier-2 anchor: `.session_backup/2026-10-30/c_t2/T2_DECISION.json` sha256 `e29bbe8a…7c40`, anchored in
`manuscript/prereg/2026-10-30_c_t2/T2_DECISION.sha256` (commit `bf4adcc`), pinned in `c_t3.py` (`T2_DECISION_SHA256`).

## 1. What tier 3 is

The three-tier method (PI-1029n): tier 1 nominated on the carve, tier 2 rehearsed once on Flickr30K val, and only the
claims that passed tier 2 with margin get the one test look. Tier 3 makes the confirmatory claims of Paper C's
English head-to-head with LMCap. Its rows sit beside C's registered Vietnamese P1 and C-EN P1-EN verdicts, which are
unchanged.

| set | tier-3 use |
|---|---|
| Flickr30K Karpathy test (1,000) | **the evaluation set, all 1,000 images, one look** (never extracted, staged, decoded or scored before) |
| Flickr30K val (1,014) and carve (1,000) | not decoded again; their images are only reference sets of the test-side near-duplicate pass (§6) |
| COCO memory (C-EN, 111,927 clusters) | the retrieval memory, unchanged; its 112,320 images' features are a §6 reference set |
| every spent or other-owner set (C-T1 PREREG §1 table) | never |

## 2. Claims (exactly the tier-2 family; nothing added, nothing removed)

From `T2_DECISION.json` (`full.family`, `m_holm` 3; val n = 1,014; pooled = carve ∪ val, n = 2,014, P at m_plan 5):

| claim | val d [95% CI] | pooled d | P(PASS on test) | tier-2 status |
|---|---|---|---|---|
| E3a Aya-Vision-8B `ret` − `lmcap_ri` | +24.63 [+21.32, +28.05] | +26.37 | 1.000 | TIER-3 FAMILY |
| E3b InternVL3-8B `ret` − `lmcap_ri` | +34.81 [+30.90, +38.83] | +37.92 | 1.000 | TIER-3 FAMILY |
| E3c Qwen2.5-VL-7B `ret` − `lmcap_ri` | +32.01 [+28.42, +35.69] | +36.37 | 1.000 | TIER-3 FAMILY |
| E1 Aya `ret` − `rand` | +5.15 [+2.34, +8.03] | +5.63 | 0.953 | VAL PASS, NO MARGIN: **never touches test** |
| E2 Qwen `ret` − `rand` | +3.12 [+0.57, +5.72] | +4.07 | 0.700 | VAL PASS, NO MARGIN: **never touches test** |

E1 and E2 are not tested and no `rand` arm is decoded on test. `c_t3.py` enforces this. On `f30k_test` only the seven
run ids in `T3_RUN_IDS` can be decoded: LMCap `ri`, three `ret` arms with the frozen k/order/template, and three `zs`
arms. `rand` runs, any other configuration and `-smoke` runs are refused. Every test decode, LMCap included, is write-once: it is refused before any
model load if its preds file or checksum exists (Codex #2). `t3` refuses a ledger row from any other run
id. `draws` still writes rand id lists for test because the shared function builds them, but they are never decoded.

## 3. Tier-3 rules (C-T1 PREREG §8, copied verbatim; C-T1 PREREG.md lines 239-250, sha256 `f1d06278`)

- **Tier-2 and tier-3 rules, fixed now (W7; copied verbatim into the tier-2 prereg, never redefined after data):**
  - val PASS per claim = point ≥ +2.0 PTB CIDEr-D AND 95% CI lower bound > 0 (C's A1 form), percentile bootstrap,
    B = 2,000, seed 0, on Flickr30K val (all 1,014 images, never used in tier 1);
  - predicted P(PASS on test, n = 1,000) from the pooled carve ∪ val per-image differences, joint = Φ(z1) + Φ(z2) − 1
    (Fréchet lower bound), z2 = d/SE − Φ⁻¹(1 − 0.05/m) with m = the size of the tier-3 family (CC-172a W12),
    labelled as such;
  - "PASS with margin" (PI-1029n, CC-171 W2 form) = val point ≥ +2.0 AND that pooled predicted P ≥ 0.98;
  - claim family = every claim NOMINATEd here AND passing with margin at tier 2. Tier-3 multiplicity: **Holm over the
    family at α = 0.05** (one-sided bootstrap p for Δ ≤ 0, Holm-adjusted); a claim PASSes at test iff point ≥ +2.0
    AND its Holm-adjusted p < 0.05. Holm is chosen now; no primary claim is named;
  - tier 3 (one look at Flickr30K test; irreversible tier, 92-98 band, PI-1029o) only if both margin conditions
    hold; no low-power route (CC-171 W4).

### 3.1 Details fixed before any test byte is read (CC-196 W7; not redefinitions)

- **D1, one-sided bootstrap p.** For claim c with per-image differences x = `ret` − `lmcap_ri` on the 1,000 test
  images: p_c = (1 + #{b : mean(x[I_b]) ≤ 0}) / (B + 1), with B = 2,000 and I = the seed-0 index matrix of `contrast`
  (`boot_idx`, the same matrix for all three claims and for the CI). The +1 correction keeps p > 0. The smallest
  possible p is 1/2,001, and Holm × 3 of that is about 0.0015 (`c_t3.py p_one_sided`).
- **D2, Holm.** Step-down adjusted p over the m = 3 family members: sort ascending, adj_(j) = max_{k ≤ j} min(1,
  (m − k + 1) p_(k)) (`holm_adjusted`). m = 3 is fixed by `T2_DECISION` (`m_holm`). `t3` refuses any other decision
  file (sha pin) or family. A claim whose arm was not decoded (cap stop, failure) is NOT RUN. It enters Holm with
  p = 1, so m stays 3, which is conservative.
- **D3, status per claim.** TEST PASS iff point ≥ +2.0 AND Holm-adjusted p < 0.05. Otherwise TEST FAIL (point
  < +2.0) or TEST FAIL (Holm p ≥ 0.05), or NOT RUN. The 95% percentile CI (B 2,000, seed 0) is printed with each claim.
- **D4, decision column = all 1,000 test images (CC-196 W7, full-datasets rule).** The near-duplicate exclusions of §6
  are computed before any decode, by the job preflight. The same decision without them is printed beside it
  (`dedup_beside`, with `n_excluded`), labelled. It never replaces the full-set result.
- **D5, W2 descriptive rows.** For each backbone, `zs` − `lmcap_ri` and `ret` − `zs` (contrast and CI only, no p, no
  status) are printed on the same 1,000 images, in full and beside the dedup row.
- **D6, no low-power route, no rescue.** Nothing is re-run, re-scored, re-seeded or re-thresholded after the look. A
  cap stop or failure leaves the missing claims NOT RUN (D2). There is no second look.

## 4. Frozen configuration (identical to C-T2 PREREG §4; no tuning)

| item | value |
|---|---|
| Aya-Vision-8B `ret` | k = 4, order last, template T1, τ = −∞ (C-T1 B1, `t_config.json` `948165b8`) → run `t3_aya_vision_8b_f30k_test-ret-k4-last-T1-mcoco` |
| Qwen2.5-VL-7B `ret` | k = 8, order first, T1, τ = −∞ → `t3_qwen25vl_7b_f30k_test-ret-k8-first-T1-mcoco` |
| InternVL3-8B `ret` | k = 4, order last, T2, τ = −∞ only (C-T2 C6) → `t3_internvl3_8b_f30k_test-ret-k4-last-T2-mcoco` |
| `zs` (W2, descriptive) | C-EN's English zero-shot prompt, all three backbones → `t3_<model>_f30k_test-zs` |
| LMCap `ri` | C-T1 §4 re-implementation unchanged (M-CLIP H-14 image→caption retrieval, K = 4, N = 3 fixed shots drawn by `seed("lmcap_shots", "f30k_test")` among clusters below the near cut for every test query, XGLM-2.9B fp16 safetensors `9e292657`, beam 3, M-CLIP re-rank, 40 new tokens) → `t3_lmcap-ri_f30k_test-mcoco` |
| memory, near cut, prompts, scorer | as C-T2 §4: COCO memory `b77e4bde`/`add1d92a`; SigLIP2 cosine ≥ 0.92 never shown; template `b329e57a`, greedy, 60 new tokens; PTB CIDEr-D (pycocoevalcap 1.2), df over test's own 5 references; paired per-image differences |
| lists | `c_t1_f30k_lists.json` `eebcd95b` (`refuse.test`, 1,000 names) |

The only per-set inputs are the set name `f30k_test`, which keys the LMCap shot draw, and the test images themselves.
The same rule was keyed on `f30k_val` at tier 2.

## 5. Arms, GPU budget, machine

Rates are the C-T2 measured seconds (M1 `gpu_seconds.tsv`, 1,014 val images, 10 arms, 2.38 GPU-h) × 1,000/1,014, with
the two `rand` rows (1,393 + 372 s) left out:

| block | arms (run order) | tier-2 s | est. s |
|---|---|---|---|
| V0 | SigLIP2 vectors of test; example lists vs the COCO memory (CPU) | 33 | 33 |
| V1 (claims) | LMCap `ri` 747; Aya `ret` 1,359; Qwen `ret` 382; InternVL3 `ret` 1,273 | 3,761 | 3,709 |
| V2 (W2, descriptive) | `zs`: Qwen 348, InternVL3 1,184, Aya 1,478 | 3,010 | 2,969 |
| **total** | | 6,804 | **≈ 6,711 s = 1.86 GPU-h** |

**Hard cap 2.5 GPU-h** (+34% over the estimate; selftest asserts estimate × 1.25 ≤ cap). Accounting is `b1.left`, every
step runs under `timeout` for the time left, and a timeout is a CAP STOP, final. V1 runs before V2, so the cap cuts the
zs arms first, last to first (Aya zs, then InternVL3 zs, then Qwen zs). A cut zs arm only removes its W2 rows (D5). A
cut claim arm makes that claim NOT RUN (D2). The CPU preflight (§6 near-dup pass) holds no GPU and is not charged. It is about 0.2-0.4 h wall: 3,064 SSCD features
at C-EN's about 0.14 s/img, and the comparison itself. The comparison was measured on the laptop at the real 1,000 ×
112,320 size, using the first 1,000 rows of `feats_memory.npz` as a pseudo-test: 11 s and 1.5 GB peak RSS, and a
positive control with 1,000 of 1,000 flagged (C1). No test byte was involved. The pass has its own 1 h wall timeout,
which is a FAULT, not a cap stop.

**Machine: M1 (machine id m3) only.** Only M1 may open the Flickr30K zip (C-T1 PREREG §2 custody). The job refuses
any other machine id and a busy GPU, and never runs concurrently with another GPU job. Wall time is about 3 h,
including staging (§8) and the pull. The schedule is in §12.

## 6. Test-side near-duplicate pass (PI-1030f: test = full near-dup)

- **Rule: W25 RULE §3, unchanged** (`manuscript/prereg/2026-10-28_w25_neardup/RULE.md`). This is the rule family
  W25-K1 applied (`AMENDMENT_W25K1.md`, commit `16c62e4`).
  - A test image is excluded if, for at least one image of a reference set: C1 the files are byte-identical; or C2
    min(pHash, dHash) ≤ 10 with the test image's mirrored hashes, AND SSCD cosine ≥ 0.5 (`build_memory.near`, C's
    registered rule, the one A-T3 r9 applied); or C3 SSCD cosine > 0.75 (SSCD authors' 90%-precision point).
  - Excluded = C1 ∨ C2 ∨ C3 (`w25.rule`, imported unchanged).
  - The count at SSCD ≥ 0.5 alone is reported and never excludes.
  - Per-criterion lists are printed, so the A-T3 reading (C1 ∨ C2 only) can be read off the same output.
- **Reference sets:**
  - (a) the COCO memory, all 112,320 images before C-EN's dedup (a superset of the 111,927 clusters shown or retrieved
    by every arm and by LMCap). Features are C-EN's `feats_memory.npz` (sha256 `caf4a621…e437`, `SHA256SUMS_feats`,
    SSCD `9f26bd4c`, head `30514a7b`), reused with no new memory byte;
  - (b) the carve (1,000);
  - (c) val (1,014);
  - (d) earlier test files: within test, the later file of a matching pair in sorted order is excluded, as in
    C-T2's within-val rule.
- **Not compared (default):**
  - Flickr30K train beyond the carve (the X5 memory, 28,000). No tier-3 arm shows it. Adding it costs about 1 CPU-h
    (Q-c).
  - Model pretraining data: unknowable, disclosed.
- **Features.** `build_memory.features` unchanged (imagehash 4.3.2 pHash/dHash + mirrored, SSCD `sscd_disc_mixup`
  TorchScript `9f26bd4c`, `small_288`). It runs in `venv-cenfeat` on M1, with the freeze checked against C-EN
  `cenfeat_venv_freeze.txt` `1a639a50`, the freeze W25 and W25-K1 used.
  - `retry_truncated` is on for the staged test, carve and val sets, as in W25-K1.
  - `features()['truncated']` (file, bytes lost) is written per set into `neardup.json` as `truncated`. It is a
    disclosure only and never an exclusion (CC-202 W3).
  - The parity call stays without `retry_truncated`, matching `build_memory.py` l.227. A parity FAULT goes back to
    the panel and is never rerun under another setting.
- **Parity (CC-190 W7 form), FAULT gate.** The first 50 COCO memory example images (sorted cluster ids, from
  `memfiles_coco.json`, staged at `cen_memory/images`) are featured on M1 and matched by sha256 to their
  `feats_memory.npz` rows. All four hashes must be exactly equal and SSCD cosine ≥ 0.999 on every row. Otherwise:
  FAULT, nothing decoded, back to the judge.
- **When and where.**
  - The pass runs in the job preflight, before V0 and before any GPU step.
  - Every input image is sha-checked against its manifest. An unreadable test, carve or val image is a FAULT.
  - It writes `/root/outputs/c_t3/neardup.json`: file names, per-set per-criterion lists and counts, the
    union `exclude`, the parity record and the input shas. No caption, no score.
  - Its sha goes into `code_at_start.sha256` and the run `SHA256SUMS`.
  - It refuses to overwrite an existing output, so it runs once.
  - On a job restart, an existing `neardup.json` is reused only if `c_t3_neardup.py check` matches it: label, rule,
    pinned inputs, the sha of each staged test/val/carve manifest, and the file's own sha against the
    `neardup.json.sha256` that `run` writes with it. Otherwise the job FAULTs (Codex #5).
- **Use.** `t3 --exclude neardup.json` prints the beside row (D4). The exclusions never change the decision column.
  No one looks at any pair, because looking would be new labelling.
- **Ceilings.** SSCD thresholds were calibrated on DISC (and Somepalli's 0.5 on generated images), not on Flickr or
  COCO. The `im.draft` decode makes the 0.75 calibration approximate (W25 RULE §8). These are disclosed.

## 7. Scoring and decision (laptop, after the pull; one call each, run once)

`$R` = the pulled `/root/outputs/c_t3/out`. `$ST` = caption stores outside the repo. `$CSV` = the pinned Flickr30K
annotation file (`395990db…ac137`). `$LED` = a new, empty ledger dir outside the repo (it holds only `test_coco.jsonl`). `$PCC` = the scoring interpreter with
pycocoevalcap 1.2 (wheel `083ed791…`), the same venv C-T2 recorded in `T2_ENV.txt`, recorded again in `T3_ENV.txt`.

```
mkdir -p $LED $ST .session_backup/2026-10-31/c_t3
$PCC scripts/c_t3/c_t3.py store --csv $CSV --what test_refs --out $ST/test_refs.json
$PCC scripts/c_t3/c_t3.py score --set f30k_test --memory coco --runs $R/t3_*_f30k_test-zs.preds.json \
    $R/t3_*_f30k_test-*-mcoco*.preds.json $R/t3_lmcap-ri_f30k_test-mcoco.preds.json \
    --refs $ST/test_refs.json --captions $ST/coco_captions.json --ledger $LED/test_coco.jsonl
$PCC scripts/c_t3/c_t3.py t3 --ledger $LED/test_coco.jsonl --t2-decision .session_backup/2026-10-30/c_t2/T2_DECISION.json \
    --run-sums $R/../SHA256SUMS --exclude $R/../neardup.json --out .session_backup/2026-10-31/c_t3/T3_DECISION.json
```
- `store`, `score` and `t3` refuse a GPU host (machine id m3/m4). This is CC-196 Codex fix 1: the laptop-only rule is
  now in code. The test references never go to M1.
- `store` keeps only test rows.
- `score` on `f30k_test` refuses, before any import or reference read (Codex #3/#4):
  - a ledger that exists, that is not named `test_coco.jsonl`, that lies inside the repo, or whose dir holds any
    other `*.jsonl` (a dev ledger dir). Scoring is therefore one call into the §7 location only;
  - a preds file whose run id is not in `T3_RUNS`, or whose spec is not exactly that id's frozen (model, arm, k,
    order, template, memory);
  - a preds file whose sha differs from the job's `.sha256` checksum written beside it on M1.

  Test rows also carry `order`, `tpl` and `preds_sha256`.
- `t3` refuses, in each case before it writes anything:
  - an existing `--out`: the decision is written once (CC-202 W2);
  - a decision file other than `e29bbe8a`;
  - a family other than the three E3 claims;
  - a ledger row from an unregistered run id (CC-196 W5(b): config identity is now checked per row, not only through
    the job hash);
  - a ledger row whose (model, arm, k, order, template, memory) is not its run id's frozen config, or whose
    `preds_sha256` differs from the job's `SHA256SUMS` line for that run (`--run-sums`; Codex #4);
  - a ledger that is not all 1,000 test images.
- The output holds ids and numbers only: per claim the test contrast and CI, the one-sided p, the Holm p and the status;
  `m_holm`; the W2 rows; and `dedup_beside`.
- With `--exclude`, `dedup_beside` is always written, with `n_excluded`, even when that is 0. With 0 exclusions the
  row equals the full row (CC-202 W2).
- `masked3` rows are scored as at tiers 1-2 and stay descriptive.
- No agent opens a preds file.
- The decision sha is anchored in `manuscript/prereg/2026-10-31_c_t3/T3_DECISION.sha256` by the gatekeeper.

## 8. Staging checklist (operator, M1; one LOG line per step, no host string)

1. M1 is free: the job before it has finished at a `.done` boundary, its GPU is idle, and no `/root/outputs/*/RUNNING`
   exists. Mirror that job first (pull-only).
2. `datasets/a_t3` (and any other dir outside `ISO_DATASETS`) is parked outside `$NCS_DATA/datasets` by a same-fs
   rename, with the tree hash taken before and after (C-T2 S1/S2 form).
3. `/root/vsps` is fast-forwarded to the commit that holds this prereg (git bundle, `--ff-only`), and both SUMS check.
4. Zip `$NCS_DATA/f30k_raw/flickr30k-images.zip` = `2ce2420c…7391`. Run `c_t3.py extract --zip <zip> --out
   /root/c_t3_stage/c_t3_f30k_test.tar` (refuses off m3; reads the 1,000 test members only; writes
   `manifest_test.json`). Untar by list into `$NCS_DATA/datasets` (`c_t3_f30k_test/images/`) and copy the manifest to
   `c_t3_f30k_test/manifest.json`. Record both shas, then delete the `.tar` and the stage dir.
5. Still staged and re-hashed:
   - `c_t2_f30k_val` (manifest `7323c1a7`, 1,014 files);
   - `c_t1_f30k_carve` (manifest `79c41b1d`);
   - `cen_memory/images` (memcheck);
   - `c_t1_mem/memfiles_coco.json` `081899c5` and `coco_captions.json` `9c830e22`;
   - `/root/outputs/c_en/cen_memory*` (C-T1 `RESTORED_SHA256`).

   If val is gone, re-extract it with `c_t2.py extract` (val only, already spent; logged) for features only.
6. Pushed from the laptop backup and sha-checked:
   - `/root/outputs/c_en/feats_memory.npz` = `caf4a621…e437` (from `.session_backup/machines/M3/root/outputs/c_en/`);
   - `$NCS_DATA/models/sscd_disc_mixup.torchscript.pt` = `9f26bd4c…` (if absent).

   `/root/venv-cenfeat` is built from `cenfeat_venv_freeze.txt` if absent; `pip freeze | sha256sum` must be `1a639a50`.
7. Model snapshots, venv-lb `685ffe2a`, venv-t1 (`T1_FREEZE` = `1766dc23…`), and venv-c1score are as at C-T2.
8. Launch `T1_FREEZE=… bash scripts/c_t3/c_t3_job.sh <HEAD>` in tmux.
9. After JOB DONE (or CAP STOP), pull-only mirror `/root/outputs/c_t3` and check `SHA256SUMS`. Then delete
   `datasets/c_t3_f30k_test` (logged in `deletions.log` and the LOG) and restore the parked dirs, tree hash equal.
   The test images exist on M1 only between steps 4 and 9.

## 9. What is printed (pre-written; PI-1029m, papers-aim-for-pass: registered results are never hidden)

- **Every claim, any outcome.** Point, 95% CI, one-sided p, Holm p and status, on all 1,000 images. Beside them: the
  dedup row and `n_excluded`, plus the W2 rows.
- **If all three PASS.** "On the Flickr30K Karpathy test split (n = 1,000, one look, preregistered), retrieval
  prompting beat our re-implementation of LMCap for each backbone (Aya-Vision-8B, InternVL3-8B, Qwen2.5-VL-7B; Holm
  over three claims at α = 0.05)." This sentence always carries the §10 E3 framing and the `zs` − `lmcap_ri` rows.
- **If a claim FAILs (point < +2.0 or Holm p ≥ 0.05).** One sentence in the results with its numbers and the
  label "registered test claim, not supported", for example "For <backbone>, the preregistered test contrast against
  LMCap was <d> [<lo>, <hi>] (Holm p <p>), below the registered bar; the claim is not supported." The row stays in the
  main results table, not only in the supplement. Its val and pooled rows are not used to argue it away. Nothing is
  re-run.
- **If a claim is NOT RUN.** "Not run (GPU cap / failure); no test result exists for this claim," with the cause from
  the job log. It is not replaced by the val result.
- **If the dedup row differs in status from the full-set row.** Both are printed, the full-set row is the result, and
  the difference is stated in one sentence.
- **E1/E2 (never tested).** Both stay dev rows from tier 2, labelled "rehearsal passed, no margin (pooled P 0.95 /
  0.70 < 0.98), not taken to test", per PI-1029m.
- **Method disclosures (CC-202 W8; commitments, written in Paper C whatever the outcome):**
  - The registered quantity (D1) is an uncentred percentile-bootstrap tail statistic with the +1 correction. It is
    "p-like": approximately the CI-inversion form of the one-sided percentile test, but it is neither an exact p-value
    under the null nor an exact CI inversion. The interpolated percentile bound and the discrete +1 count can disagree
    at the boundary. The decision uses this registered statistic only. The method (C-T1 §8 verbatim) is unchanged
    (Codex #1).
  - The pooled P(PASS) of 1.000 is a planning value that includes the carve nomination data (CC-196 W6,
    winner's-curse label).
  - Only tier-3 rows are confirmatory.
  - The near-dup parity call omits `retry_truncated` by design: it matches how the pinned memory features were
    built (`build_memory.py` l.227).
  - The near-dup pass uses the W25-K1 rule call (`w25.rule` with `build_memory.near`) but not W25-K1's C1 sha lists
    or its truncated bound. Truncated images are recorded per set in `neardup.json` as a disclosure only (§6).

## 10. Wording commitments for Paper C (C-T2 §9 carried forward, verbatim; plus CC-196 W5/W6)

- **E3 (W2, CC-191 r1/r2):** E3 is written as the reviewers' requested same-data head-to-head with a published
  training-free baseline (meta-review item 3), never as evidence for the retrieval prompt. `zs` − `lmcap_ri` is
  printed beside every E3 row (carve: Aya −13.8, Qwen +18.2, InternVL3 +37.9). The LMCap row is labelled
  "re-implemented, this study, dev" with the deviations listed: one shown caption per memory cluster (not all
  captions), C's SigLIP2 near cut also removes LMCap's closest neighbours, 40 new tokens, fp16. The robustness bound
  is stated: at LMCap's published XM3600-en level (45.2) E3 would still be about +17.6 / +30.5 / +30.2.
- **Aya RICES (W3, CC-191 r3), sentence used as is:** "Aya-Vision's interleaved multi-image prompt was run once and
  not validated; its row is shown and not interpreted." No claim about image versus text demonstrations rests on Aya.
- **InternVL3 `ret` − `rand` (W4):** "descriptive, not a §8 candidate" (consistent with OpenFlamingo's Flickr-30K
  reversal), never "a dropped claim".
- **X2 (W5):** `ret` − `rand` turns negative for every backbone after masking 3-grams shared with the shown examples,
  so the CIDEr gain travels through borrowed reference-like wording (lexical/style transfer). Masking is biased
  against `ret` (it also removes correct borrowed words), so X2 does not show the gain is spurious. C claims nothing
  beyond lexical/style transfer from CIDEr gains; P2 object-precision claims stand as registered.
- **X5 (W5):** the memory swap is a style- and size-confounded descriptive row (rand drops as much as ret, captions get
  longer, the shown caption is Flickr's first reference, 28k vs 112k clusters), never "in-domain memory hurts".
- X3 (P_cm, Vietnamese) stays descriptive C support, not a hallucination-metric finding.
- Qwen RICES beats text-only `ret` on the English carve (+8.5; −0.5, n.s., on OV-dev-B); C's text-only design is
  justified by cost (about 5× GPU time) and the Vietnamese parity, not by accuracy.
- **Tier-3 additions:**
  - **W2 on test.** The test `zs` − `lmcap_ri` rows replace the carve figures in the E3 sentence. On val they were
    Aya −16.0, Qwen +11.6, InternVL3 +30.5. With the E3 contrasts that means:
    - for InternVL3 most of the E3 margin is already present zero-shot;
    - for Aya all of it comes from the retrieval prompt.

    The sentence says this per backbone, whatever the test numbers turn out to be.
  - **CC-196 W6.** The pooled P(PASS) was a planning value that included the carve nomination data (winner's-curse
    direction). C-T1 carve rows are never called confirmatory. C1/C2 of C-T2 are pre-data clarifications. Only tier-3
    rows are confirmatory.
  - **CC-196 W5 (record).** C-T2's laptop-only scoring rested on custody plus the m3/m4 hook, and its keys omitted
    k/order/template. Tier 3 closes both in code (§7). The M1 end date 2027-03-04 is from OPS-1031m1.
  - **Near-duplicates.** "Test images that were byte-identical or near-duplicates of any retrieval-memory, carve, val
    or earlier test image were identified before decoding (n = N of 1,000, W25 rule); the result on all 1,000 images
    is the registered result, and the result without them is shown beside it."

## 11. Binding-rule compliance

- **Three-tier method.** One test look, only for the three tier-2 family claims. E1/E2 and every `rand` arm are refused
  on test in code. There is no tuning surface: every configuration is frozen, and seeds are keyed by set name.
- **Data.** No new human labels; no AI label used as evidence. Full official split: the decision is on all 1,000 test
  images, and the near-dup row is only printed beside it.
- **Captions.** No Flickr30K, COCO, OpenViIC, KTVIC or UIT-ViIC caption text appears in any repo file. Preds and stores
  live under `/root/outputs/c_t3` and outside the repo. Ledgers, `neardup.json` and the decision hold ids and numbers
  only. No agent opens a preds file.
- **Hosts and e-mail.** No host, IP or port in repo files; M1 is named only by its alias and machine id. No personal
  e-mail in any request or file.
- **Cost.** ≤ 2.5 GPU-h on M1. The drafting agent made no commit, no GPU use and no machine access. It did not extract
  or stage any test image. Commit goes through the gatekeeper after the launch panel.

## 12. M1 schedule (CC-202 ruling 8; A-T3 tier-3 decode must start on M1 by 2026-11-07T00:00Z)

- **GPU.** M2 was deleted on 2026-10-31 at 05:45 VN (OPS-1031m2del), so M1 is the only GPU. C-T3 (about 3 h)
  and A-T3 tier 3 (about 19 GPU-h) both fit on M1 before A's 11-10 freeze. No second rental is needed for them
  (CC-202 ruling 9).
- **Order on M1:**
  1. The current M1 job, to its `.done` boundary.
  2. **C-T3**, as soon as W4, the gatekeeper commit and W5 (Codex) are done. It takes about 3 h wall: staging
     ~0.5 h, near-dup ~0.3 h, GPU 1.86 h, pull + cleanup ~0.2 h.
  3. A-T3 tier 3, once its own gates are met (W6, judge GO, TEST_RESERVED; CC-197), and only after §8 step 9.
  4. MT4 tier 1, after both.
- **No preemption.** Once started, C-T3 runs to JOB DONE or CAP STOP. A-T3 tier 3 starts only after §8 step 9:
  `c_t3_f30k_test` deleted and logged, and `datasets/a_t3` restored with an equal tree hash. Flickr30K test images
  are therefore never on M1 during A's block. This agrees with §8 step 9 and with the custody bullet below.
- **Latest C-T3 start: 2026-11-05T12:00Z.** If C-T3 has not started by then, it waits until A-T3 tier 3 is DONE.
  M1 never idles for it (keep-queue-full).
- **Fallback (a').** If A-T3 tier 3 is launch-ready (W6 committed, judge GO, TEST_RESERVED) before C-T3 is
  committed, A goes first and C-T3 follows A's restore. The same no-preemption rule applies in both orders.
- **No custody conflict.** C-T3 deletes `c_t3_f30k_test` and restores `datasets/a_t3` (§8 step 9) before A-T3 tier
  3 starts. A's guard therefore never sees Flickr30K test files, and C's guard never sees `a_t3/`.

## 13. Open items and judge questions (each with a recommended default)

**Ruled by CC-202** (GO-with-fixes 3/3, 93%, option (a)): Q-a yes, Q-b union, Q-c no, Q-d 2.5 GPU-h, Q-e +1. These
are now binding. W8 is a binding paper commitment (§9 "Method disclosures"). The questions are kept below as asked.

- **Q-a (D4).** Should the decision be on all 1,000 images with the near-dup row beside it, per CC-196 W7 and the
  full-datasets rule, or should test-side drops be removed from the decision column, as A-T3 does? Recommended: all
  1,000. Default: all 1,000.
- **Q-b (§6 rule).** W25 union C1 ∨ C2 ∨ C3 (default, the W25-K1 reading), or C1 ∨ C2 only (A-T3 r9's
  `build_memory.near`)? Per-criterion lists are printed either way. Recommended: union.
- **Q-c (§6 sets).** Add Flickr30K train beyond the carve (28,000 images, about 1 CPU-h on M1) as a reference set?
  Recommended: no, because no tier-3 arm shows it. Default: no.
- **Q-d (cap).** 2.5 GPU-h (+34%)? Recommended: yes.
- **Q-e (D1).** Should the +1 bootstrap p (CC-196 W7) be used instead of the plain proportion? Recommended: +1.
- O1: launch panel (3 judges + Codex, ≥ 92) on this file, `diff scripts/c_t2/c_t2.py scripts/c_t3/c_t3.py`,
  `c_t3_neardup.py` and `diff scripts/c_t2/c_t2_job.sh scripts/c_t3/c_t3_job.sh`.
- O2: gatekeeper regenerates both `SHA256SUMS` at commit (draft sums are present now) and makes no `__pycache__`.
- O3: §8 items 5-6 checked on the current M1 (val still staged, `feats_memory.npz` pushed, venv-cenfeat, SSCD).
