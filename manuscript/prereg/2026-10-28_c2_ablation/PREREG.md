# Paper C, C-2: pre-registration of the memory-size, k and guard-threshold ablations on OV-dev-B

**Label: DEV-B MECHANISM, NON-CONFIRMATORY.** Ruled by CC-126 W12 and ruling 5; PI-1026ac Q8 (C-2 and B-1 run before MT4 Gate 1). No C-2 decode, score or read of an archived τ row exists before this file, its subset list and the code of §12 are committed by the gatekeeper and judge-read. **This file registers AB-τ before anyone reads the archived InternVL3 τ rows** (W12).

| field | value |
|---|---|
| Paper | C (TALLIP). A mechanism section on the dev set and a supplement table; **no C-2 row enters C's abstract or contributions** (W12), and no C-2 row changes any registered verdict of C (P1, P1b, P2, XM-a, XM-b, S-zf, §8.4) |
| Starting draft | `manuscript/ken/K16_PREREG_DRAFT_C2.md` (Ken, not binding). Changed here: option (a) with the written shared-rand identity, the P-M outcome definitions, the §6 condition, no fix arm, the replay gate, the cap semantics, parity on OV-dev-B |
| Carried over | C's stage-2 prereg `manuscript/prereg/2026-10-22_c_stage2/PREREG.md` (`6d039398…`), `frozen_config.json` (`2f0c32be…`), the stage-1 `lists.json` (`5c479f03…`) and design; C's test prereg bindings (`2026-10-25_c_test/PREREG.md` §0) where they concern outputs and captions |
| Pinned list (this folder) | `c2_memory_subsets.json` sha256 `ae5f67319c1063c10574feda68e6fecdd88ed3045876d5d1710a0ede034715f0` (cluster ids only; producer `scripts/c2_ablation/c2.py subsets`) |
| Code | `scripts/c2_ablation/` (§12), `SHA256SUMS` there |
| Machine | M3 only |
| Written | 2026-10-27/28 on the laptop, CPU only. The stage-2 ledger, decide files, preds and example files were not opened (§11) |

## 0. Bindings

1. **OV-dev-B only (925 images, `lists.json` `sets.ov_dev_b`).** Never OV-test (2,001), XM-test2500, XM-dev500, KTVIC dev299 or any test image. `stage2.py check-host --block ov` runs before the job; `stage2.manifest2` refuses any other set in every decode, item and score step; every output lies under `/root/outputs/c2_ablation/`.
2. **The frozen configuration is not re-chosen.** Qwen2.5-VL-7B: k 8, order first, tail T1, τ = −∞; InternVL3-8B: k 4, order last, tail T2, τ = 0.10, verifier Qwen3-VL-8B; memory 8,190 clusters, SigLIP2 so400m, near cut 0.92, greedy, 60 new tokens. C-2 never calls `pick()`; every row is a description of mechanism on dev.
3. **One look.** Each C-2 run is decoded once and scored once; `decide` runs once after the last step or a CAP STOP. Nobody reads a C-2 caption, ledger row or score, or an archived τ row, before `decide`; monitoring uses counts, times, return codes and GPU seconds (CC-103 W10).
4. **No rescue.** No C-2 row reinterprets XM-a FAIL, P1b-InternVL3 or H_G (a registered negative). The τ sweep describes the cost of deletion; it is no new guard claim.
5. **No fix arm** in any ablation (W12).
6. No dataset caption in any committed file; outputs are never committed; C-2 commits numbers, ids and sha256 only.
7. **Isolation:** never concurrent with a C-EN test decode or `--stage` (CC-124 r3), with B-1, or with a G-RL pilot (§8).

## 1. Preconditions

### 1.1 Before this prereg is committed
1. The judge panel has read this file, `c2_memory_subsets.json` and `scripts/c2_ablation/`; the gatekeeper's caption scan and host grep find 0 hits.
2. `c2.py --selftest` passes on the laptop (synthetic data only).

### 1.2 Before any M3 step (checked by `c2_job.sh`)
1. HEAD equals the gatekeeper commit; clean tree; `manuscript/prereg/2026-10-22_c_stage2/SHA256SUMS` (stage-2 code), `scripts/c2_ablation/SHA256SUMS` and this folder's `SHA256SUMS` verify; the stage-1 shas are checked by `stage2.py` at import.
2. `/root/outputs/c_stage2/SHA256SUMS` verifies on M3 (the stage-2 runs, `ledger.jsonl` `be716482…`, `decide_ov.json` `92fdbf0e…`, `ex_ov_dev_b.json` `072b17d1…`, `emb_ov_dev_b.npz` `5ad23a67…`, the InternVL3 guard cache); `/root/outputs/c_stage1/emb.npz` = `59e65f6f…`.
3. Venvs: `venv-lb` `685ffe2a…` (decode, verifier), `venv-c1score` `4b81b6b6…` (scoring, kit B), openjdk 11.0.32.1. **The scorer is exercised before any GPU step:** `c2.py --selftest` in both venvs, and in the scoring venv `score2.py --selftest --kit-b scripts/kit_b` and `decide2.py --selftest` (as the stage-2 job). Model snapshots: Qwen2.5-VL-7B `cc594898…`, InternVL3-8B-hf `259a3b64…`, Qwen3-VL-8B `0c351dd0…` (`lb.check_snapshot`).
4. Staged by the laptop chain `scripts/c2_ablation/c2_chain.sh stage` (CC-128 W9), as stage 2 and C test did; it also restores `outputs/c_stage2` and `c_stage1/emb.npz` from the mirror if absent (sha-checked): the 925 OV-dev-B images (sha 925/925), the 1,836-key OV-dev annotation subset (`550cfe06…`), and the two memory-caption sources (`ktvic/train_data.json` `72ee9b57…`, `openviic/uit-openviic-annotation-train.json` `d757520e…`). After the block: the images deleted and the annotation restored to its 911-key state (CC-099 clean-up).
5. **Monitoring rule (CC-128 W10):** until `decide.json` exists, no agent opens a decode or score log, a preds file, the C-2 ledger or the stage-2 ledger, on M3 or in the mirror; monitoring reads only `job.log`, `gpu_seconds.tsv`, return codes and counts. C-EN steps run only through `cen_chain.sh`; the job starts only when `m3_clear` passes (W11).
6. Guard before every GPU step: M3, idle GPU, committed HEAD, clean tree (`grl/common.host_ok`); C-EN not running and no protected C-EN set staged (`common.m3_clear`); inside tmux; no `cen*` tmux session; no other `/root/outputs/*/RUNNING`.

## 2. The three ablations

Notation: per image i of OV-dev-B, cider_s = kit-B stripped CIDEr-D (stage-2 PR2 §6.1, unchanged); Δ_m(·)_i = cider_s(ret_m, ·, i) − cider_s(rand_m, ·, i) at the frozen τ_m (Qwen −∞, InternVL3 0.10); pooled Δ_i = ½(Δ_qwen,i + Δ_internvl,i).

### 2.1 AB-M: memory size (10 / 30 / 100%), option (a)

- **Subsets:** 10% = 819 and 30% = 2,457 of the 8,190 clusters, prefixes of one permutation of the sorted cluster ids by `random.Random(build_memory.seed("ablation", "memory", "0"))` (i.e. `paperC|ablation|memory|0`), so 10% ⊂ 30% ⊂ 100%. Pinned in `c2_memory_subsets.json`. Retrieval inside a subset is `build_memory.exemplars` unchanged (top-8 by cosine, ties by cluster id, near cut 0.92), on the stage-1 memory vectors and the stage-2 OV-dev-B query vectors.
- **New runs:** `ret` at 10% and 30% for both backbones (4 decodes; InternVL3's 2 through the verifier at τ 0.10). The 100% point is the stage-2 row.
- **Shared rand control (W12; replaces K16 C2 l.111 "assumption not checkable").** `rand` is the stage-2 100% `rand` row for every memory size. Then, identically, DiD_M = Δ(10%) − Δ(100%) = (ret_10 − rand) − (ret_100 − rand) = **ret_10 − ret_100** per image (asserted in code). The identity that makes the shared control valid: a cluster-uniform random subset S of the memory, drawn independently of the query, and then k clusters drawn uniformly from S, gives k clusters that are marginally uniform over the full memory; so `rand` drawn from a seeded cluster-uniform nested subset has the same distribution as `rand` drawn from the full memory, and per-size `rand` arms (~2 GPU-h) buy no information in expectation (CC-126 J-note). The near cut removes the same clusters in both cases up to the subset intersection; this second-order difference is disclosed, not modelled. **The identity is exact only marginally over the seeded subset draw;** for the one fixed subset S used here it is approximate, and the subset's source composition against the full memory (§11 item 6, `decide.json` `composition`) is the check (CC-128 W8b).
- **Source share (reported):** the cluster composition of each subset by source (from `lists.json` members, ids only; §11 item 6) and each ret row's share of shown examples whose cluster has an OpenViIC member (`score2.extras` `src_share`).
- **Style check (reported):** rand − zs at 100% per backbone and pooled, from the stage-2 rows (W12).
- Also reported: the mean top-1 cosine of the retrieved cluster at each size; per backbone Δ_m and DiD_m; InternVL3's ret rows at τ = −∞ at each size.

**Prediction P-M (pooled, SESOI +2.0, C's registered SESOI):**
- M1: CI upper bound of DiD_M < 0 (shrinking the memory to 10% detectably lowers the gain);
- M2: DiD_M ≤ −2.0;
- M3: point estimates monotone, Δ(10%) ≤ Δ(30%) ≤ Δ(100%).
- **Outcome:** HOLDS iff M1 ∧ M2 ∧ M3; **FAILED iff ¬M1** ("P-M fully failed"); PARTIAL otherwise. A missing run makes AB-M INCOMPLETE (no outcome).
- Prior information: C's OV-test dose-response by cosine tertile was not monotone (+4.40 / +2.95 / +6.13, §11), so P-M is a risky prediction.

### 2.2 AB-K: number of examples k

- **Grid:** k ∈ {2, 4, 8} for both backbones, order, tail and τ frozen, 100% memory; `ret` and `rand` at each k are prefixes of the stage-2 eight-example lists (`ex_ov_dev_b.json`). The frozen k (Qwen 8, InternVL3 4) is the stage-2 row. **k = 2 is kept** (W12 "k = 2"; Ken's Q1 option (b), dropping k = 2, is not adopted). New: Qwen k2, k4 and InternVL3 k2, k8, ret and rand each (8 decodes; InternVL3's 4 through the verifier).
- **Prediction P-K (Qwen2.5-VL only; label: "shaped by stage-A dev299 selection"):** K1 Δ_qwen(2) ≤ Δ_qwen(4) ≤ Δ_qwen(8) (points); K2 Δ_qwen(8) − Δ_qwen(2) ≥ +2.0; K3 the CI lower bound of that difference > 0. HOLDS iff K1 ∧ K2 ∧ K3, else NOT HELD. Stage A chose k8-first-T1 for Qwen on KTVIC dev299, so P-K is not blind to a k comparison on another dev set.
- InternVL3 and pooled: Δ at each k reported, no prediction (stage A chose k4 for InternVL3).
- Reported: mean syllables, 4-gram copy share against the full memory's 4-grams (`score_set` `copy4_memory`) and near-verbatim share at each k.

### 2.3 AB-τ: guard threshold for InternVL3 (CPU only)

- **Grid:** τ ∈ {−∞, 0.00, 0.10, 0.20, 0.30, +∞} on the **stage-2 InternVL3 ret and rand decodes** of OV-dev-B, from the rows the unchanged stage-2 scorer wrote to `ledger.jsonl` (`be716482…`). 0 GPU-h. The −∞ and 0.10 rows are published (C Table 13); the 0.00, 0.20, 0.30 and +∞ rows were archived unread ("not registered for any claim", C test PREREG §6.4) and are registered here, before anyone reads them. Only `decide` reads them, once.
- **Prediction P-τ:** Δ_internvl(τ) = ret_τ − rand_τ.
  - (i) Δ non-increasing over −∞, 0.00, 0.10, 0.20, 0.30, +∞ (point estimates, ties allowed);
  - (ii) the deletion cost on ret is more negative than on rand at every finite τ (0.00, 0.10, 0.20, 0.30): mean(ret_τ − ret_−∞) < mean(rand_τ − rand_−∞) (points). Algebraically (ii) ⟺ Δ(τ) < Δ(−∞) at each finite τ, so it is a strict, anchored form of (i) (§14 Q3);
  - (iii) the CI lower bound of Δ(+∞) ≤ 0.
  - HOLDS iff (i) ∧ (ii) ∧ (iii), else NOT HELD.
- The −∞ and 0.10 values must equal the replay (§4 step 1), else AB-τ is INCOMPLETE.
- **Disclosure carried into every P-τ report (CC-128 W8a):** the −∞ and 0.10 points, and (ii) at τ 0.10 (−5.43 vs −2.48, C Table 13), were known before this registration (§11 item 2); only the 0.00, 0.20, 0.30 and +∞ points are new information. P-τ is kept as Ken wrote it; replacing it now would set a criterion after part of the data was seen (CC-128 ruling 2).
- Reported per τ, for ret and rand: neighbour-only rate, rejected per image, fallback and deletion rates, neighbour-only precision and Σm.
- Qwen's τ rows in the ledger are **not read and not reported** (Qwen is frozen at −∞; §14 Q4).

### 2.4 "§6 explains backbone dependence"

C's §6 may say that C-2 explains why the retrieval gain depends on the backbone **iff P-τ (i) and (ii) hold AND P-M is not FAILED** (HOLDS or PARTIAL) (W12). Otherwise §6 says that the dev ablations do not explain it, and UPGRADE_PLAN §6's rule applies (C-EN FAIL on both English sets and no C-2 explanation → C is submitted as an in-domain baseline study with its limits stated). Either way the sentence is labelled "on the development set (OV-dev-B)".

## 3. Scorer and bootstrap

- Scorer: `score2.set_rows` (stage-1 `score_set` + stage-2 extras, unchanged): kit B (RDRSegmenter, `protocol_pilot` CIDEr-D, stripped column `cider_s` for every rule; as-written and PTB columns reported), matcher v2, gold = the union of an image's OV-dev-B references, df over the 925-image set. Only the `ca_` rows are kept; the zero-shot and NN rows are stage 2's.
- Bootstrap: paired image bootstrap, B = 2000, percentile 95%, `numpy.random.default_rng(0).integers(0, 925, (2000, 925))`, **one index matrix for every CI** (`score.boot`, drawn fresh per call, identical each time); image order = the sorted ids that every row stores; pooling averages the per-image differences over the backbones, then resamples; DiD is resampled on the same matrix.
- Multiplicity: three predictions (P-M, P-K, P-τ), one test each, uncorrected; every other row is descriptive with an uncorrected CI. No C-2 "holds" or "not held" enters C's abstract or contributions.

## 4. Procedure (frozen; `scripts/c2_ablation/c2_job.sh`)

1. **Replay (CPU), before any decode (W12).** `c2.py replay` reads the stage-2 ledger, keeps only the OV-dev-B rows of InternVL3 at τ ∈ {−∞, 0.10} and of Qwen at τ = −∞ (every other row, Qwen's τ rows included, is dropped as it is read; CC-128 W7), recomputes with `decide2.gate` and `score.boot` (unchanged), and asserts at 2 dp: pooled ret − rand **+6.04 [4.54, 7.58]** (C Table 11, `journal_draft_C/06_results.md` l.146; `AUDIT_2026-10-26.md` l.139, from `decide_final.json :: ov_dev_b.gate`); Qwen **+9.67 [7.68, 11.72]** (Table 11, l.147); InternVL3 at τ 0.10 **+2.41 [0.57, 4.26]** (Table 11, l.148; Table 13, l.165); InternVL3 at τ −∞ **+5.36 [3.53, 7.12]** (Table 13, l.165, column "`ret` − `rand` at τ = −∞", i.e. ret@−∞ minus rand@−∞, which is what `replay` computes); and the three frozen-τ values exactly equal to `decide_ov.json` (`92fdbf0e…`). Any difference is a STOP before any decode.
2. **AB-M exemplars (CPU):** `c2.py exemplars --pct 10|30`.
3. **AB-M decodes (GPU):** Qwen, one process: **parity** first, then ret m10, m30; then InternVL3 the same. **Parity (CC-101 rule, on OV-dev-B):** the frozen stage-2 ret run re-decodes the first 52 OV-dev-B images (13 / 26 whole batches at b = 4 / 2, C test's E4_N) through the C-2 decode path; ≥ 95% of captions and 100% of prompt sha256 identical to the stage-2 preds, else STOP. Counts only are written.
4. **AB-M verifier (InternVL3):** items of its C-2 runs (`guard.items` against the stage-2 zero-shot); Qwen3-VL-8B (`guard.hf_verifier`, `guard.fill`, unchanged) into a C-2 cache that starts as a sha-checked copy of the stage-2 InternVL3 cache, so an (image, class) item verified in stage 2 is not asked again (the verifier score does not depend on which examples were shown).
5. **AB-K decodes (GPU):** Qwen k2, k4 (ret, rand), then InternVL3 k2, k8 (ret, rand); then their verifier pass.
6. **Score (CPU), then decide (CPU) once**; `SHA256SUMS` of the output folder; mirror and sha-confirm; the CC-099 clean-up (§1.2 item 4).

## 5. Run grid (12 decodes, priority order)

| ablation | backbone | runs (`ca_` prefix) |
|---|---|---|
| AB-M | Qwen2.5-VL-7B | ret k8 first T1, memory 10%, 30% |
| AB-M | InternVL3-8B | ret k4 last T2, memory 10%, 30% (verified, τ 0.10) |
| AB-K | Qwen2.5-VL-7B | ret, rand at k2, k4 |
| AB-K | InternVL3-8B | ret, rand at k2, k8 (verified, τ 0.10) |
| AB-τ | InternVL3-8B | none (stage-2 rows, CPU) |

Run ids: `ca_<model>_ov_dev_b-<arm>-k<k>-…[-m10|-m30]` (`c2.py runs`).

## 6. Cap (5 GPU-h, hard 6) and priority

| item | basis (measured on M3, stage-2 OV-dev-B block, `outputs/c_stage2/job.log`, 2026-10-22) | GPU-h |
|---|---|---|
| 6 Qwen decodes | 4 arms × 925 in 3,429 s (13:37:34–14:34:43Z) = 857 s per run | 1.43 |
| 6 InternVL3 decodes | 4 arms × 925 in 6,022 s (14:34:43–16:15:05Z) = 1,506 s per run | 2.51 |
| parity (52 images × 2) | the same per-image rates | 0.04 |
| 2 extra model loads per backbone | not measured; budgeted at 2 min each | 0.07 |
| InternVL3 verifier (6 runs, cache-seeded) | stage 2: ret + rand + fix items in 382 s (16:34:21–16:40:43Z); at most twice that | ≤ 0.21 |
| **expected** | | **≈ 4.3** |
| cross-check | C test on M3, per image-arm Qwen 0.69 s, InternVL3 1.24 s (C-EN PREREG §10, `c_test/gpu_seconds.tsv`) | ≈ 3.1 |

- InternVL3's k8 runs show twice its frozen k of examples and may run longer; Qwen's k2/k4 runs are shorter. The expectation leaves ≈ 0.7 GPU-h under the soft cap.
- The stage-2 rates were measured on the 10-22 M3, before the 10-26 rebuild and re-rent; the host may differ (the C test of 10-25/26 ran on the rebuilt RTX 3090 M3, the cross-check row).
- Rows of an INCOMPLETE ablation that exist are still reported per backbone (`decide` computes every per-backbone Δ whose runs exist; only the pooled prediction is withheld).
- **Cap counting across a reboot (CC-128 W6):** each GPU step writes `NAME start EPOCH` to `gpu_seconds.tsv` before it runs and `NAME SECONDS` after; a start without an end is charged to the next start, or to the next cap check if last (`c2.py used_seconds`), so a reboot can only over-count.
- **Cap semantics:** the GPU seconds of every GPU step (step wall time) are summed in `gpu_seconds.tsv`; **no GPU step starts once 5 GPU-h are used; a running step is killed (timeout) when the total reaches 6 GPU-h.** Either is a **CAP STOP, final** (`CAP_STOP.json`): no GPU step after it; score and decide run on what exists; an ablation whose grid is not complete is INCOMPLETE and its prediction is not judged; its finished rows are reported.
- **Priority if the cap binds:** AB-τ (CPU, always) → AB-M (Qwen, then InternVL3, then its verifier) → AB-K.

## 7. Decision outputs

`decide.json` holds: AB-M (pooled Δ at 10/30/100%, DiD_M and its CI, M1–M3, outcome, per backbone, source share), AB-K (Δ per k per backbone, P-K with K1–K3 and its label, style and copy rows), AB-τ (Δ(τ), costs, (i)–(iii), outcome, guard rates), rand − zs at 100%, the §6 condition, the mean top-1 cosine per memory size, the subset composition, the sha256 of the stage-2 ledger, the C-2 ledger and the code.

## 8. STOP and kill rules

- Replay mismatch → STOP before any decode.
- Parity < 95% identical or any prompt sha256 different → STOP.
- Stage-2 host check fails (a test, XM or OIV7 file on M3; not 925/925 OV-dev-B; not the 1,836-key subset) → STOP.
- Qwen3-VL answer-position stop (`guard.answer_position_check`): registered and final (`VERIFIER_STOP.json`, exit 3); InternVL3's rows at τ 0.10 of the ablations not yet verified are INCOMPLETE; no fallback to −∞ for a prediction (the −∞ rows are still reported). Once `VERIFIER_STOP.json` exists the InternVL3 AB-K decodes are skipped (CC-128 R1).
- Any other GPU or CPU step failure → JOB STOP to the judge; a crash resumes with the same code; rows written stay unchanged.
- **Lock convention:** `/root/outputs/c2_ablation/RUNNING` (O_EXCL) for the whole job; the job refuses to start and the guard refuses every GPU step while any other `/root/outputs/*/RUNNING` (G-RL, B-1) exists or a `cen*` tmux session runs; the job runs inside tmux, so `cen_chain.sh` cannot start a C-EN step during it.
- After decide: no rerun, no extended grid, no new arm. A change goes into a dated amendment (§13) before the affected output exists.

## 9. Reporting

- One supplement table "mechanism on the development set (OV-dev-B)", dated, with every row of §7, whatever the outcome.
- **P-M FAILED:** "On dev, shrinking the memory to 10% did not detectably reduce the retrieval gain": the "near examples" mechanism is not supported; style or format from any in-domain example may be named as an alternative, as a description only. **PARTIAL:** the measured DiD with its CI, "below the SESOI" or "not monotone" as applicable.
- **P-K NOT HELD:** "The gain did not grow with k for Qwen2.5-VL on dev (a k comparison shaped by stage-A selection)".
- **P-τ NOT HELD:** the part that failed is named. The C post-hoc remark that random in-domain examples give most of the gain stays a labelled post-hoc sentence (CP-116a X2); C-2 may feed it with the rand − zs row, never title, abstract or contributions.

## 10. Data, staging and outputs

- On M3, the laptop chain stages §1.2 item 4 from the releases (`stage2.py subsets` makes the 1,836-key subset locally, values unchanged), and removes them after the block. No other caption file reaches M3. Outputs under `/root/outputs/c2_ablation/` (example lists, preds, items, cache, ledger, replay, parity, decide); mirrored by gpu_backup; never committed except numbers and sha256 through the gatekeeper.

## 11. What the author saw (and did not)

1. **C's registered results, as quoted in Ken's draft and CC-126:** OV-test P1 +4.49 [3.52, 5.57]; P1b Qwen +8.33 [7.01, 9.76]; InternVL3 (τ 0.10) +0.66 [−0.68, 1.99]; P2 PASS both (+5.41, +1.57); rule L not triggered (0.074, 0.039); 2,001 images +4.46; XM-a FAIL +0.70 [−0.45, 1.97], Qwen +3.15, InternVL3 −1.75 [−3.35, −0.09], XM-b PASS +0.59; S-zf +14.30 (OV) / +11.99 (XM) against fix +3.47 / +2.53; the OV-test dose-response +4.40 / +2.95 / +6.13 (not monotone; relevant to P-M); §8.4 InternVL3 τ = −∞ +3.71 [2.29, 5.14] OV, +0.18 XM.
2. **Stage B (OV-dev-B, the C-2 set):** pooled +6.04, Qwen +9.67, InternVL3 +2.41 (τ 0.10) / +5.36 (τ −∞); Table 13 deletion costs ret −5.43, rand −2.48 at τ 0.10; H_G not passed (precision +2.91 [0.46, 5.31], cost −4.01); Σm 714 → 80. So **two of the six AB-τ points (−∞, 0.10) are known**, and (ii) is known to hold at τ 0.10; only 0.00, 0.20, 0.30 and +∞ are unread.
3. **Stage A (KTVIC dev299):** k ∈ {2, 4, 8} × order × tail was swept and chose k8-first-T1 (Qwen) and k4-last-T2 (InternVL3); AB-K is not blind to a k comparison (the P-K label). The Qwen dev299 τ rows exist; their values were not read.
4. **Stage-2 run record and job log** (times and shas only: the per-block GPU seconds and step timestamps used in §6), the stage-2 and stage-1 code, the C test and C-EN preregs and code as templates; the M3 mirror's file listing of `outputs/c_stage2/` and the sha256 of its ledger, decide, emb and example files.
5. CC-126 (W12, ruling 5, J-notes), PI-1026ac, Ken's K16 draft.
6. **`lists.json` cluster composition (ids and source tags only):** 8,190 clusters = 6,017 OpenViIC-only, 2,133 KTVIC + OpenViIC, 40 KTVIC-only; the pinned subsets: 10% = 600 / 212 / 7, 30% = 1,805 / 643 / 9.
7. **Published C text read:** `journal_draft_C/06_results.md` l.140–170 (the H_G paragraph and Tables 11–13), to source the replay values; `AUDIT_2026-10-26.md` l.139 (grep line). No other part of `journal_draft_C` was opened.
8. **Opened for metadata only, no caption:** while writing the CC-128 chain, the top-level keys and image count of KTVIC `train_data.json`; C test's E4 dev299 preds file `ct_e4_c1_qwen25vl_7b_…-ret-k8-first-T1.preds.json` on the M3 mirror, of which only `gpu`, `machine_id` and `cuda` were printed; the top-level keys and set sizes of `lists.json` and the source tags of its clusters' members.
9. **Not opened:** `ledger.jsonl`, `decide_ov.json`, `decide_final.json`, `verified.jsonl`, any stage-2 preds or example file's content, any caption or reference. No exemplar or cosine of a memory subset was computed.

## 12. Code (scripts/c2_ablation/)

| file | sha256 (first 8) | role | where |
|---|---|---|---|
| `c2.py` | `d66d500e…` | subsets, check, grid, guard, lock, cap arithmetic, replay, exemplars, decode (C-2 provenance, parity), items, verify, score, decide, `--selftest` | laptop / M3 |
| `c2_job.sh` | `682be221…` | the M3 job: preflight, lock, replay, AB-M, AB-K, verifier passes under the cap, score, decide | M3 |
| `c2_chain.sh` | `fbc3d95d…` | laptop operator chain (CC-128 W9): dry-run, stage (incl. the c_stage2 / emb.npz restore), run, cleanup; refuses on any tmux session, any `/root/outputs/*/RUNNING` or a failed m3_clear; W10 rule in its header | laptop |

Full shas in `scripts/c2_ablation/SHA256SUMS`. Reused unchanged (imported, sha-checked against the stage-2 SHA256SUMS): `scripts/c_stage2/stage2.py` (`frozen`, `spec`, `manifest2`, `references2`, `check_host`), `decode2.py` (`load_emb1`, `build_exemplars`, `prompts`), `guard2.py` (`item_paths`), `score2.py` (`kit2`, `set_rows`), `decide2.py` (`gate`, `get`, `rid`, `cider_diff`); through them `scripts/c_stage1/` (`build_memory.exemplars`, `seed`; `decode_icl`; `guard.items`, `hf_verifier`, `fill`; `score.boot`, `latest`, `load_cache`), `scripts/lb/decode_hf_vlm.py`, `scripts/kit_b/`, and `scripts/grl/common.py` (`host_ok`, `m3_clear`). `c2.py decode_one_c2` follows `decode2.decode_one` / `ctest.decode_one_t` with C-2's label, schema and prereg in the provenance. `c2.py --selftest` uses synthetic data only (the grid, nested subsets, the replay against decide2's synthetic ledger, every outcome of P-M, P-K and P-τ, the §6 condition, INCOMPLETE on a missing run, the host guard, locks and cap).

## 13. Amendments

**Amendment 1 (2026-10-28, PI-1026ai, CC-132 slot ruling): machine change only.** The job may run on M4 (dev-only, never holds test images) as well as M3; the laptop chain takes a required `GPU=m3|m4` that selects the backup-config entry, the machine-id check and the mirror folder (`.session_backup/machines/M3|M4/`). `GPU=m3` behaves as before. On M4, `m3_clear`'s C-EN test-side record requirement is skipped (a staged `cen_` set or a running C-EN process still refuses, in the chain and in the job guard; the chain's `pgrep` pattern is bracketed so it cannot match its own remote shell, CC-133 W1), and the chain adds a scan of `$NCS_DATA/datasets` that refuses any test-split path and any file whose sha256 is a test-side sha: the union of `exclusion.json` (5,180), C-EN's three test-side records (Karpathy test 5,000, Karpathy val 5,000, NoCaps val 4,500) and the stage-1 `lists.json` `refuse.image_sha256` (6,599, mostly OV-test), 22,260 shas in all, and the chain stops unless every source count is exact (CC-133 W2, W3) (none is allowed). No frozen value, rule, list, cap or prediction changes. The GPU-h estimates were measured on M3-class RTX 3090 hosts; rates on M4 may differ; the caps are unchanged. The stage-1/2 inputs are restored from the M3 mirror; the C-2 outputs mirror to `.session_backup/machines/M4/`.

**Amendment 2 (2026-10-28, CC-134): test-side union and upload fixes; no frozen value changes.** STOP-M4-1: C-2's first M4 stage stopped at the test-side scan before any GPU step. Amendment 1's union wrongly included all of `lists.json` `refuse.image_sha256` (6,599), which contains C's own dev sets (924 OV-dev-B, 500 XM-dev500); every hit was a dev image, no test image reached M4, and M4 was cleaned. The test-side part of that list is now its 6,599 shas minus the 1,424 dev-set shas in `lists.json` `sets`, i.e. 5,175 (OV-test, XM-test2500 and the other refused images), so the union is 21,336 shas, not 22,260; the chain checks |refuse| = 6,599 and the dev overlap = 1,424 exactly. Before any upload the chain checks that the staged image shas hit this union only at the allowed list: none (this is what Amendment 1's "(none is allowed)" meant). The chain's upload loops ran ssh inside a `while read` loop, which read the loop's stdin; `rsha`/`put` now read `/dev/null` and the number of uploaded files is checked. No frozen value, rule, list, cap or prediction changes.

**Amendment 3 (2026-10-28, CC-135): provenance field fix in `c2.py`; no frozen value changes.** STOP-M4-2: the first GPU step (`dec_qwen_M`, the 52-image parity decode) stopped with rc=1 after 107 GPU-s, because `decode_one_c2` built its provenance without the `parity_slice0` field that `scripts/lb/decode_hf_vlm.py`'s output check requires; no output, parity file or comparison was written or read. `decode_one_c2` now runs the same solo pass on the first batch and records `parity_slice0` exactly as `scripts/c_stage2/decode2.py` does; the output check and `scripts/lb` are unchanged. `c2.py --selftest` now checks statically that the provenance holds every field the output check requires. The new `c2.py` sha is in §12 and `scripts/c2_ablation/SHA256SUMS`. The 107 GPU-s stay charged to the cap (the restage restores `gpu_seconds.tsv` from the mirror), and the stale parity partial on M4 is deleted unread before the restage. No frozen value, rule, list, cap or prediction changes.

None after commit. Before commit, CC-128 (GO-with-fixes) W6–W10 and R1 are applied in this file and the code: the reboot-safe cap count, the Qwen-τ replay filter, the P-τ and shared-rand disclosures, the laptop chain, the monitoring rule and the InternVL3 AB-K skip after a verifier stop.

## 14. Open questions for the judge

1. **Q1 "k = 2" in W12** is read as "AB-K keeps k = 2" (Ken's Q1 recommendation; option (b) rejected), giving the grid {2, 4, 8} for both backbones. Confirm.
2. **Q2 "P-M not fully failed"** is defined as M1 (CI_hi(DiD_M) < 0), i.e. HOLDS or PARTIAL. An alternative is "DiD point < 0". Confirm.
3. **Q3 P-τ (ii)** is algebraically Δ(τ) < Δ(−∞) at each finite τ, so it is nearly implied by (i) (strict and anchored at −∞), and it is already known to hold at τ 0.10 (§11 item 2). Keep as written (Ken), or replace by a CI rule on cost_ret − cost_rand?
4. **Q4 Qwen τ rows** of stage 2 (Ken's Q3: report as descriptive) are not read or reported here. Confirm, or register them now as descriptive rows.
5. **Q5 parity on OV-dev-B** (first 52 images of the frozen ret runs against the stage-2 preds) instead of KTVIC dev299 (Ken §1.5): it needs no extra staging and checks the exact comparison C-2 makes (new M3 decodes against the 10-22 rows), but it is a second decode of 52 OV-dev-B images (counts only). Confirm.
6. **Q6 verifier-cache reuse:** the C-2 InternVL3 cache starts as the stage-2 cache, so shared (image, class) items keep their stage-2 verifier scores. Confirm.
7. **Q7 cap semantics:** "cap 5, hard 6" = no GPU step starts after 5 GPU-h; a running step is killed at 6. Confirm.
8. **Q8 lock visibility:** `cen_fetch.no_pilot` sees only `grl_pilot/RUNNING`; C-EN is kept out of C-2 by the tmux rule. Amend C-EN to refuse any `/root/outputs/*/RUNNING`?
9. **Q9 source share** is reported two ways (subset cluster composition; per-row share of shown examples with an OpenViIC member). Is a per-source split of Δ also wanted (it would be a post-hoc subgroup row)?
10. **Q10 laptop chain:** ruled by CC-128 W9; written as `scripts/c2_ablation/c2_chain.sh` (dry-run / stage / run / cleanup); it still needs a judge code read and the gatekeeper commit before the first M3 run.
11. **Q11 file size:** `c2.py` exceeds aislop's 400-line guideline (warning, not fixed); splitting it would add pinned files.
