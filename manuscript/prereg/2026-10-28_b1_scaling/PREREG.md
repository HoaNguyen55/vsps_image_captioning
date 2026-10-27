# Paper B, B-1: pre-registration of the multi-seed data-scaling curve on KTVIC dev300

**Label: DEV CURVE. Development split only; never a test result.** Ruled by CC-126 W11 and ruling 5; PI-1026ac Q7 (retrain all 15 adapters on M3, cap 20 GPU-h, primary CI_lo(b) > +1) and Q8 (B-1 runs before MT4 Gate 1, after C-2). No training, decode or score of this registration exists before this file, its lists and the code of §12 are committed by the gatekeeper and judge-read.

| field | value |
|---|---|
| Paper | B (LRE). B-1 gives one planning constant for the data plan of the proposal; it makes no method claim and changes no registered B verdict |
| Predecessor | Tier-3 S5, `manuscript/prereg/2026-10-18_tier3_S5.md` (frozen 2026-10-18T08:50:37Z; `.json` sha256 `39a8433b…`, `.md` `a5f7f6ad…`). Its rule (l.61) is B-1's primary rule |
| Starting draft | `manuscript/ken/K16_PREREG_DRAFT_B1.md` (Ken, not binding). Changed here: the primary rule (W11), the +2.0 role, the scorer pin, the incomplete-seed rule, the cap arithmetic |
| Pinned lists (this folder) | `b1_lists.json` sha256 `c4926ed2f73068897fae17bc0093bb6b8c7de94ac82c0fbe2995dbf0af7b10c5` (ids only; producer `scripts/b1_scaling/b1.py lists`) |
| Code | `scripts/b1_scaling/` (§12), `SHA256SUMS` there |
| Machine | M3 only (`/root/.vsps_machine_id` = `m3`; RTX 3090 24 GB, as the C-test E4 provenance records) |
| Written | 2026-10-27/28 on the laptop, CPU only. No caption, prediction file content or reference was opened (§11) |

## 0. Bindings

1. **Dev300 only.** Every point is decoded and scored on KTVIC dev300 (300 KTVIC train images, `data/splits/ktvic_dev300.txt`; KTVIC has no official val). KTVIC test is closed (B-F1, `2026-10-20_b_f1_final_stack.md`) and B-1 never reopens it: no KTVIC test file is on M3 (the guard refuses `$NCS_DATA/datasets/ktvic*/test*`), and the job file may not contain the test split's file name (`b1.py check --job`, S5's `JOB_FORBIDDEN`).
2. **"Dev curve" label, mandatory.** Every B-1 number in any paper, supplement, proposal or slide carries "on the development split (dev300)". It is never called a test, held-out or generalisation result. Dev300 is the gate set of every B lever and of S1–S5 (§11 item 3).
3. **One look.** Each adapter is trained once and decoded once; `score` and `decide` run once, after the last GPU step or a CAP STOP. Nobody reads a CIDEr-D, a caption or a prediction file before `decide`; monitoring uses counts, times, return codes and GPU seconds (CC-103 W10).
4. **No selection.** Seeds 42, 43, 44 and levels L1–L5 are fixed here. No seed, level, scorer, prompt or rule is chosen after any output exists.
5. **No external data.** No OpenViIC, UIT-ViIC or translated image enters training (R14-4; S5 §4).
6. **No caption in any committed file.** Outputs (preds, adapters, ledgers) are never committed; B-1 commits ids, numbers and sha256 only.
7. **Isolation.** Never concurrent with a C-EN test decode or `--stage` (CC-124 r3), or with C-2 or a G-RL pilot (§8).

## 1. Preconditions

### 1.1 Before this prereg is committed
1. The judge panel has read this file, `b1_lists.json` and `scripts/b1_scaling/`; the gatekeeper's 6/8-gram caption scan and identity/host grep find 0 hits.
   - **Byte twins (disclosure, CC-130 W3).** (a) The official KTVIC train split contains two images byte-identical to KTVIC test images: train 3589 (`00000003589.jpg`, sha256 `bd5ea1bc723cbe731d0049d1e42a48055fbcff53f44157c701a8c4d690906261`) = test 1335, in L5 only; train 7511 (`00000007511.jpg`, `dc1cd6988daf5ece6fdcacc0535e442387b0244512b7fbf288d75880e1738f9d`) = test 507, in L2–L5. They stay in training, as in S5, n2 P1_dev and every earlier KTVIC-train model; B-1 never decodes or scores KTVIC test; they are exempted by name, path and sha in the guard and the chain (`b1.TRAIN_TEST_TWINS`; CC-130, amending CC-128 W9(b)). Found by the chain dry-run on 2026-10-27, before any B-1 output. (b) The dev twin: dev300 image 2004 is byte-identical to train image 4487, which is in L5 only (and in S5's and n2's full P1_dev training). The primary stays on the full dev300; a registered sensitivity row masks image 2004 (§6, §9).
2. `b1.py --selftest` passes on the laptop (synthetic data only).
3. Run order (not a commit condition): CC-126 ruling 5 lists C-2 before B-1 as the tie-break; any committed, ready job fills an M3 gap (W10).

### 1.2 Before any M3 step (checked by `b1_job.sh`)
1. HEAD equals the gatekeeper commit; tracked tree clean; `scripts/b1_scaling/SHA256SUMS` and this folder's `SHA256SUMS` verify; `b1_lists.json` at its pin; S5's pinned code unchanged (`train_stage2.py` `29312ef7…`, `build_gold_sft.py` `18e7909f…`, `evaluate.py` `a68d5682…`, `train_rl.py` `bd5743bb…`, `ktvic_dev_split.py` `b4adfb4c…`, `rl_reward.py` `3b18b7a3…`, `rl_report.py` `f92faa61…`, `object_prf.py` `6b711280…`, `rescap/chair.py` `e47d249a…`, `checkpoint_resume_hook.py` `05466ef5…`; S5 JSON `code_at_head`).
2. `/root/vsps/.venv` freeze `7332d343…` (setup_gpu.sh H_VS: torch 2.5.1+cu121, transformers 4.51.3, peft 0.21.2, S5's pins). Base `Qwen/Qwen2.5-VL-7B-Instruct` at `cc594898…` in the HF cache, the five shards at S5's sha256, `HF_HUB_OFFLINE=1`; the n2 adapter `p1dev_s42` at `227a3312…` (Step 0 only); KTVIC `train_data.json` at `72ee9b57…` (`b1.py check --machine`). **The scorer is exercised before any GPU step:** openjdk 11.0.32.1, and `b1.py check --kit-b` loads kit B through `c_stage1/score.kit`, asserts the protocol-card jar (`9e2811cd…`) and runs RDRSegmenter (java) and Cider on one synthetic pair in `.venv` (CC-128 W5).
3. Guard before every GPU step: `/root/.vsps_machine_id` = `m3`, idle GPU, committed HEAD, clean tree (`grl/common.host_ok`); C-EN's test-side records complete, no protected C-EN set staged and no C-EN process (`common.m3_clear`); no file named `test*` under `$NCS_DATA/datasets/ktvic*/` and no image there whose sha256 is one of the 558 KTVIC test images (`exclusion.json` `image_sha256.ktvic_test`), except the two named train twins at `datasets/ktvic/images/00000003589.jpg` and `00000007511.jpg` with exactly their pinned sha (a test-named copy, a twin under any other path, or a third hit refuses; CC-130 W1); inside tmux; no `cen*` tmux session; no other `/root/outputs/*/RUNNING` lock.
4. Uploaded by the laptop chain `scripts/b1_scaling/b1_chain.sh stage` (CC-128 W9), sha-checked by the job: KTVIC `train_data.json` and the 3,769 train images (never test); S5's three dev300 preds files (`b0ecf307…`, `a394053d…`, `1e183383…`) under `/root/outputs/b1_scaling/s5_preds/`.
5. Usage guard headroom for a ~12 h block (`usage_check.sh`, run by the chain).
6. **Monitoring rule (CC-128 W10).** evaluate.py writes CIDEr-D into `dec_*.log` and the result JSONs during the job. Until `decide.json` exists, no agent opens a `dec_*.log`, a result JSON or a preds file, on M3 or in the gpu_backup mirror; monitoring reads only `job.log`, `gpu_seconds.tsv`, return codes and counts. C-EN steps run only through `cen_chain.sh`; the job starts only when `m3_clear` passes (W11). **Hook rule (CC-130 W4):** while `sitecustomize.py` exists on M3, no `evaluate.py` or `train_stage2.py` process starts outside `b1_job.sh`; the hook lives only between `b1_chain.sh stage` and `cleanup` (which removes it first), and the staged KTVIC images make every `grl/common.guard` refuse in that window (CC-130 r5).

## 2. Populations (ids only)

| level | training images | rule | ids sha256 | sft.jsonl sha256 |
|---|---|---|---|---|
| L1 | 216 | 3469 // 16 | `89c5db07…` (new) | recorded once at build (§4 step 2) |
| L2 | 433 | 3469 // 8 | `a2bc69e2…` (new) | recorded once at build |
| L3 | 867 | 3469 // 4 | `0d18dfbd…` = S5 f25 | `c140600e…` = S5 f25 |
| L4 | 1,734 | 3469 // 2 | `a42f86b7…` = S5 f50 | `c350c296…` = S5 f50 |
| L5 | 3,469 | the split file | `006080b4…` = `data/splits/ktvic_train_minus_dev300.txt` | `97187974…` = n2 `gold_p1dev` (S5 sources) |

- **One shared permutation (W11):** L1–L4 are prefixes of `train_rl.schedule(ids of ktvic_train_minus_dev300.txt, 3469, 42)`, S5's one seeded order, so L1 ⊂ L2 ⊂ L3 ⊂ L4 ⊂ L5 and L3/L4 are S5's subsets byte for byte (asserted by `b1.py lists`). The sizes are `3469 // 2**(5 − j)`; for L3/L4 this equals S5's `floor(3469 × pct / 100)`. No level holds a dev300 image (asserted). The permutation is the same for all three seeds; the seed changes LoRA initialisation and batch order only.
- **Dev:** dev300 (`ktvic_dev300.txt`, md5 `e1af9069…`), with its five KTVIC train references per image (`ktvic_dev_split.py --json-dir`, as S5).
- **Points:** 5 levels × 3 seeds = **15 adapters, all retrained on M3** (PI-1026ac Q7); no earlier adapter enters the fit. Plus Step 0 (the n2 `p1dev_s42` re-decode) and one zero-shot decode (no adapter).

## 3. Models and recipe (S5, unchanged)

- Base `Qwen/Qwen2.5-VL-7B-Instruct` revision `cc594898137f460bfe9f0759e9844b3ce807cfb5` (apache-2.0), 5 shards at S5's sha256.
- Recipe P1_dev (job 35_a): `train_stage2.py --stage sft --data gold_b1_<L> --epochs 2 --seed <s> --loss-mask assistant`, LoRA r 16 / α 32 / dropout 0.05 on the LM layers, last checkpoint only, save_steps 200 (the hook). The card rule of `train_stage2.py` gives 512 vision tokens at 4-bit on a 24 GB card; the job requires "loss mask: assistant", "save_steps=200" and "512 vision tokens, 4-bit" in every training log.
- Decode: `evaluate.py --model qwen2.5-vl-7b --adapter <run> --split dev_data.json --prompt short` with `NCS_DATASET=ktvic_dev`, bf16, greedy, its defaults; **short prompt only** (W11; S5's prompt). The zero-shot point is the same command without `--adapter`.

## 4. Procedure (frozen; `scripts/b1_scaling/b1_job.sh`)

1. Preflight §1.2; take the lock `/root/outputs/b1_scaling/RUNNING` (O_EXCL; removed on exit).
2. Data (CPU): write the five ids files from `b1_lists.json` (sha-asserted); `ktvic_dev_split.py --verify --json-dir $NCS_DATA/datasets/ktvic_dev`; `build_gold_sft.py --annotations train_data.json --out gold_b1_<L> --images-file <ids file>` for each level; L3–L5 must equal the registered sha256, else STOP; the L1/L2 sha256 are written once to `data/sft_L1_L2.sha256` before any training and must stay equal on resume.
3. **Step 0 (GPU):** re-decode `p1dev_s42` (n2 adapter) on dev300 on M3; at least 95% of the 300 captions identical to the registered n2 decode, taken from S5's byte-identical copy `s5_preds/p1dev_s42_redecode-dev300-short.preds.json` (sha256 `1e183383…`, equal to n2's `data/results/rl/p1dev_s42-dev300-short.preds.json`; CC-128 W4), else STOP to the judge (CC-101 rule). Counts only are written (`step0.json`); nothing is selected. S5's own Step 0 was 300/300 identical.
4. Zero-shot decode (GPU): `b1_zeroshot`.
5. **Points, seed-major (GPU):** s42 L1→L5, then s43 L1→L5, then s44 L1→L5; for each, train (skipped if `metrics.jsonl` exists; a crash resumes from the hook's checkpoints) and decode (skipped if its result exists; a decoded but unscored file is scored by evaluate.py's recovery, never decoded twice).
6. `score` (CPU, §5), then `decide` (CPU, §6–§7) once; `SHA256SUMS` of the output folder; mirror and sha-confirm by the laptop chain.

## 5. Scorer

- **Decision column: kit B, final punctuation stripped** (W11; C's PR2 §6.1 convention): VnCoreNLP-1.2 RDRSegmenter (jar `9e2811cd…`, B's protocol card), lower-cased, `protocol_pilot.Cider` (pycocoevalcap CIDEr-D re-implementation), the candidate's trailing punctuation tokens stripped by `punctuation_audit.strip_trailing_punct_tokens`; ×100; df from the 300 images' own five references. Loaded through `scripts/c_stage1/score.py kit()` (pins `protocol_pilot.py` `6aee4282…`, `punctuation_audit.py` `a7e80240…`). As-written CIDEr-D is reported beside it. Per-image values are kept so every CI is a paired image bootstrap.
- This is **not** S5's scorer (S5 used `rl_report.dev_scores`, word-level pycocoevalcap CIDEr-D). B-1's numbers are therefore not S5's numbers.
- **S5 re-score (disclosed look):** S5's three existing dev300 preds (f25, f50, the p1dev_s42 redecode) are re-scored with the same kit-B column in the same `score` call, so that the S5 slope can be printed on B-1's scale. This is a look at existing dev predictions whose S5-scorer values are known (§11); it is descriptive and gates nothing.
- **Objects (reported, never gating):** object F1 against the union of the five references' classes (exact classes, `object_prf.scores`) and CHAIR_i (`rescap.chair`), computed by `scaling_probe.object_counts` as in S5.
- **Length:** mean syllables per point (`rl_reward.syllables`); per seed, if |len(L1) − len(L5)| / len(L5) > 0.10 the seed's slope is printed with "not separated from length" (non-gating label).
- Scoring runs in `/root/vsps/.venv` (S5's venv), as a separate process from generation.

## 6. Statistical model

Notation: y_{s,L} = mean stripped CIDEr-D on dev300 of seed s at level L; x_L = log2(N_L), N = 216, 433, 867, 1734, 3469 (x from 7.75 to 11.76).

- **Primary fit (P-B1):** y_{s,L} = a_s + b·x_L + ε, one common slope b, one intercept per seed (seed fixed effects), over the complete seeds (§7.4). On this balanced grid b equals the mean of the per-seed OLS slopes (asserted by the selftest against an explicit dummy regression). b is "stripped CIDEr-D per doubling of KTVIC training images".
- **CI (image sampling):** paired percentile bootstrap over the 300 dev images, B = 2000, `numpy.random.default_rng(0).integers(0, 300, (2000, 300))`, **one index matrix for every point and every CI**; each draw recomputes every point's mean from its per-image values (df fixed, as S5) and refits b. It covers image sampling; seed variance enters through the three seeds' intercepts and slopes, not through the CI.
- **Per seed:** b_s by OLS on the five points of seed s, with its image CI (same matrix); min, max, and a 95% t-interval over the three b_s (df = 2, t = 4.303), descriptive.
- **Curvature (reported):** c of y = a_s + b·x + c·x² with seed fixed effects, with its image CI; and b_top = mean_s (y_{s,L5} − y_{s,L4}) with its CI.
- **Zero-shot:** its stripped CIDEr-D is printed and plotted at N = 0 and **never fitted** (log2 0 is undefined; the selftest asserts that changing it leaves b unchanged).
- **Sensitivity row, registered (CC-130 W5; CPU only, descriptive, no rule, no verdict):** "dev300 minus image 2004 (byte twin of L5 train image 4487)". Each point mean is taken over the other 299 images; each bootstrap replicate uses the registered index matrix with the draws of image 2004 dropped from that row (the mean over the remaining draws). The pooled b and its CI are reported, with the S5 rule's label applied descriptively; the same mask is applied to the two replication rows (S5's redecode is full P1_dev and was also trained on 4487). Fixed here, before any B-1 output.
- **Replication rows (descriptive, no rule):** the S5 slope over L3–L5 from the kit-B re-score of S5's preds, and the new M3 seed-42 slope over L3–L5, each with its image CI from the same matrix.

## 7. Registered rules

| name | estimand | rule | role |
|---|---|---|---|
| **P-B1 (primary)** | pooled b, image CI | S5 l.61, clauses in their written order: **FUND_EXTERNAL_IMAGE_DATA if CI_lo(b) > +1; CLOSE_DATA_VOLUME_LEVERS if b < +1; INCONCLUSIVE otherwise** (reported as PASS / FAIL / INCONCLUSIVE) | the verdict |
| proposal-use floor | b | the proposal may use b as a planning constant only if P-B1 is PASS **and** b ≥ +2.0 | disclosed floor, not a gate on the verdict |
| **P-B1-seed (registered secondary)** | min_s b_s | STABLE iff every b_s > +1 | the sentence the proposal quotes (§9) |
| F1 slope (reported) | pooled F1 slope | S5 §7's frozen F1 prediction [0, +2] is printed as hit or miss | never gating |

1. **Source of the primary rule.** S5 l.61, registered before any S5 output (2026-10-18). B-1 re-applies it, with the pooled multi-seed slope in place of S5's single-seed slope and kit B's stripped column in place of S5's scorer.
2. **The +2.0 floor was set after S5's +9.40 was known.** It comes from UPGRADE_PLAN §6 (written 2026-10-27, after supplementary_B §S7 reported +9.40); it has no independent source (CC-126 J-note on B-1 SESOI). It decides only whether the proposal may quote b as a planning number; it never changes PASS/FAIL/INCONCLUSIVE.
3. **No point prediction is registered.** Ken's draft guessed b in [+5, +12] ("no source"); it is recorded here as Ken's unsourced guess and is not a rule. S5's frozen CIDEr-D prediction [+1, +4] (whose n-gram proxy read KTVIC test references, S5 §11) is not re-used.
4. **Incomplete seeds (added here, judge to confirm, §14 Q1).** Only seeds with all five levels trained, decoded and scored enter the fit. P-B1 has a verdict only with ≥ 2 complete seeds; with fewer it is NO VERDICT and the points are reported. A seed with a missing level is printed per level, labelled incomplete.

## 8. Cap, STOP and kill rules

| condition | consequence |
|---|---|
| Step 0 < 95% identical captions | STOP to the judge; nothing is trained |
| an ids file, L3–L5 sft.jsonl or L1/L2 recorded sha differs | STOP |
| a training log lacks "loss mask: assistant", "save_steps=200" or "512 vision tokens, 4-bit" | STOP |
| any GPU step fails (non-zero, not a timeout) | JOB STOP to the judge; re-run resumes with the same code; rows written stay unchanged |
| **cap 20 GPU-h** | the GPU seconds of every train and decode step (step wall time) are summed in `gpu_seconds.tsv`; each GPU step runs under `timeout` for the time left; a step does not start with < 60 s left; a timeout or exhaustion is a **CAP STOP, final**: `CAP_STOP.json`, no GPU step after it, then `score` and `decide` run on what exists (§7.4) |
| a guard refusal before a GPU step (C-EN running, another lock, a test file, busy GPU) | JOB STOP; the lock is released; restart only after the condition clears |
| a result file with `n_images` ≠ 300 (or not a short-prompt dev300 decode) | JOB STOP to the judge: `b1.py score` refuses it (`dev_preds`), so no ledger and no decide exist until the judge rules (CC-128 W2) |
| a point with no result file (a CAP STOP before its decode) | the point is missing; its seed is incomplete and leaves the fit (§7.4) |

- **CAP STOP and seeds (CC-128 W3).** A CAP STOP yields a P-B1 verdict on the ≥ 2 seeds that are complete, or NO VERDICT with fewer; S5's single-seed rule is never substituted. The seed-major order (§4 step 5) completes seed 42 first, then 43, then 44. W11's "else reuse with host labels" branch is not taken: all 15 adapters are retrained on M3 (PI-1026ac Q7).
- **Cap counting across a reboot (CC-128 W6).** Each GPU step writes `NAME start EPOCH` to `gpu_seconds.tsv` before it runs and `NAME SECONDS` after it returns; a start without an end (a reboot or kill mid-step) is charged from its start to the next start, or to the time of the next cap check if it is the last line (`b1.py used_seconds`), so the cap can only over-count downtime, never under-count.
- **Resume hook (CC-128 W1).** The preflight requires `/root/vsps/.venv/lib/python3.10/site-packages/sitecustomize.py` at sha256 `05466ef5…` (= `scripts/checkpoint_resume_hook.py`, S5's pin), else STOP before any GPU step; `b1_chain.sh stage` installs it as a symlink and `cleanup` removes it.
- **Lock convention.** `/root/outputs/b1_scaling/RUNNING` is held for the whole job (O_EXCL, removed on exit). The job refuses to start, and the guard refuses every GPU step, while any other `/root/outputs/*/RUNNING` exists (G-RL `grl_pilot/RUNNING`, C-2 `c2_ablation/RUNNING`) or any `cen*` tmux session runs; the job runs inside tmux, so `cen_chain.sh` (which refuses while any tmux session exists) cannot start a C-EN step during it.
- After `decide`: no rerun, no extra seed, level, prompt or scorer. Any change goes into a dated amendment (§13) committed before the affected output exists, and is reported next to every number it touches.

## 9. Reporting

- Every one of the 15 points is printed in a supplement table (stripped and as-written CIDEr-D, F1, CHAIR_i, mean syllables, train_runtime, host M3), with the zero-shot point, Step 0's identical share and the two replication rows, under the caption "dev curve (dev300)".
- **The proposal quotes, and only if P-B1 is PASS and b ≥ +2.0:** "On the KTVIC development split (dev300), each doubling of the training images added b [lo, hi] CIDEr-D (n complete seeds, 2 or 3, common slope); the slope exceeded +1 for every seed (min b_s = …)", with b_s printed for exactly those seeds — the second clause only if P-B1-seed is STABLE; otherwise "…; it did not exceed +1 for every seed (b_s = …, …, …)".
- **Dev-twin reading (pre-written, CC-130 W5):** if the S5 rule applied to the sensitivity row gives a different label from P-B1's verdict, every quote of b adds "not robust to one dev/train duplicate image (b without it = … [lo, hi])"; the verdict itself stays P-B1's.
- **FAIL:** "On dev300, doubling the KTVIC training data changed CIDEr-D by b [lo, hi] per doubling, below +1": every KTVIC data-volume lever is closed and reported as a finding (S5 §8). **INCONCLUSIVE:** no external-data spend; reported. No alternative analysis is offered in place of a registered row.
- B's framing is unchanged (CC-126 W3); a B-1 result enters B only as a dev-curve supplement row and the proposal's data-plan constant.

## 10. Data, staging and outputs

- KTVIC train annotation (`train_data.json` `72ee9b57…`) and images are staged to `$NCS_DATA/datasets/ktvic/` by the laptop chain (CC-099: each job stages its own data); no test file. Outputs under `/root/outputs/b1_scaling/` (decodes, logs, `ledger.json`, `decide.json`, `step0.json`, `gpu_seconds.tsv`) and adapters under `$NCS_DATA/runs/b1_s<seed>_<L>/`; mirrored by gpu_backup; never committed except `decide.json` numbers and sha256 lists through the gatekeeper.

### 10.1 GPU budget (measured rates)

| item | basis (measured) | GPU-h |
|---|---|---|
| 15 trainings | 2 epochs × (216 + 433 + 867 + 1,734 + 3,469) × 3 seeds = 40,314 samples at 1.128 / 1.125 samples/s (S5 `train_runtime` 1,537.2 s for 1,734 samples and 3,081.3 s for 3,468; O-2308423, RTX 3090, 4-bit, 512 vision tokens; S5 log `train_p1dev_s42_f25/f50.log`) | 9.93–9.95 |
| per-training overhead | S5: log close minus `train_runtime` ≈ 10 s per run (file mtimes); budgeted at 1 min × 15 | 0.25 |
| 17 dev300 decodes (15 + Step 0 + zero-shot) | 0.69 s/image × 300 (S5 queue log `01_t3_4_s5_data_scaling.log` l.41/134/253); ≈ 215 s wall per decode with model load (S5 file mtimes) | 1.02 |
| **expected** | | **≈ 11.2** |
| **cap (PI-1026ac Q7)** | 1.8× the expectation | **20** |

The rates are from another RTX 3090 host (O-2308423); M3's training rate has not been measured. Ken's 13.4 used a 0.15 h decode guess; the measured decode is 0.06 h.

## 11. What the author saw (and did not)

1. **S5, all of it** (the prereg, its JSON, `scaling.json`): the decision FUND_EXTERNAL_IMAGE_DATA; CIDEr-D per point 125.52 (f25), 128.71 (f50), 144.33 (f100 redecode); b = +9.40 [4.87, 13.89]; F1 per point 52.22 / 53.04 / 54.57, F1 slope +1.18 [−0.06, 2.41]; CHAIR_i per point 0.258 / 0.263 / 0.233, slope −0.0127 [−0.0285, +0.0034]; Step 0 300/300 identical (CIDEr-D difference 0.0); the sha256 of S5's result, preds and adapter files; the S5 training logs' `train_runtime` lines and the queue log's decode-rate lines and timestamps. **B-1 is therefore not blind to S5**: L3–L5 at seed 42 repeat S5's design on a new host; only L1, L2 and seeds 43, 44 are new information (CC-126 Q7).
2. **B-F1 member scores (KTVIC test):** P1-dev seeds 42 / 43 / 44 at 144.18 / 144.86 / 147.60 CIDEr-D (mean 145.55), MBR-3 145.15, D_MBR −0.391, P1-R 147.96–148.66 (supplementary_B §S7 l.282–284). These are test-set numbers of the L5 recipe at the three B-1 seeds; they shaped no B-1 design choice and enter no B-1 analysis.
3. **Dev300 is not new:** it is the gate set of P1, fuse2, WiSE-FT, S1–S5 and the Qwen3-VL guard; every B adapter has been decoded on it.
4. The permutation is the one S5 and RL S3 used (S5 §11).
5. CC-126 (W11, ruling 5, J-notes), PI-1026ac, Ken's K16 draft and the C-EN and C-test preregs as templates. The M3 mirror's file listing (names only) of `b_f1_ktvic_test/`, which is never uploaded to M3 (setup_gpu.sh exclusion).
6. **Opened for metadata only, no caption:** S5's three `*.provenance.json` files (machine O-2308423, git head `ca7812ce…`, hook and train_stage2 sha256, result sha256); the top-level keys of one S5 result JSON (`name`, `split`, `n_images`, …, `predictions`; its values were not printed); C test's E4 dev299 preds file `ct_e4_c1_qwen25vl_7b_…-ret-k8-first-T1.preds.json` on the M3 mirror, of which only `gpu` (NVIDIA GeForce RTX 3090), `machine_id` and `cuda` were printed (the source of "M3 is an RTX 3090").
7. **Byte twins (CC-130):** the four file names, ids and sha256 of §1.1 (train 3589 = test 1335, train 7511 = test 507, dev 2004 = train 4487) and their level membership (3589 in L5; 7511 in L2–L5; 4487 in L5); the twins were found by hashing image bytes, and within-train byte-duplicates (7 groups) were counted by the judge; no caption or reference was opened.
8. While writing the CC-128 chain: the top-level keys of KTVIC `train_data.json` (`images`, `annotations`), its image count (3,769) and the key names of one `images` entry (`id`, `filename`); no annotation was printed. The chain reads file names only from it.
9. **Not opened:** any caption, any prediction text, any dev300 or test reference, any KTVIC annotation. The L1/L2 sft.jsonl were not built on the laptop (their sha256 is recorded at the M3 build, §4 step 2).

## 12. Code (scripts/b1_scaling/)

| file | sha256 (first 8) | role | where |
|---|---|---|---|
| `b1.py` | `f586621e…` | lists, check, ids, sft pins, guard, lock, cap arithmetic, Step 0, score, decide, `--selftest` | laptop / M3 |
| `b1_job.sh` | `41668755…` | the M3 job: preflight, lock, data, Step 0, zero-shot, 15 points under the cap, score, decide | M3 |
| `b1_chain.sh` | `6a6ecb1c…` | laptop operator chain (CC-128 W9): dry-run, stage, run, cleanup; refuses on any tmux session, any `/root/outputs/*/RUNNING` or a failed m3_clear; W10 monitoring rule in its header | laptop |

Full shas in `scripts/b1_scaling/SHA256SUMS`. Reused unchanged: `scripts/scaling_probe.py` (S5's `subsets` rule via `train_rl.schedule`, `ols`, `decide`, `object_counts`, `corpus`, `dev_refs`, `write_once`, `base_snapshot`, `verify`, `JOB_FORBIDDEN`), `scripts/c_stage1/score.py` (`kit`, `JAR_SHA256`), `scripts/kit_b/` (pinned), `scripts/grl/common.py` (`host_ok`, `m3_clear`), `train_stage2.py`, `build_gold_sft.py`, `evaluate.py`, `ktvic_dev_split.py`. `b1.py --selftest` runs on synthetic data only (the fixed-effects identity, the three S5 outcomes and their clause order, the floor, the seed secondary, the zero-shot exclusion, the incomplete-seed rule, curvature, the host guard on raising / missing / readable paths, the locks and the cap); it opens no caption and no dataset file (it reads the S5 prereg JSON for its rule text).

## 13. Amendments

None after commit. **Deviation, CC-130 (before commit):** CC-128 W9(b) is amended: the two named KTVIC train/test byte twins are staged and exempted by name, path and sha (W1, W2); the dev twin is disclosed and a registered sensitivity row added (W3, W5); the hook is removed first in cleanup and the hook operator rule added (W4). Before commit, CC-128 (GO-with-fixes) W1–W6 and W9–W10 are applied in this file and the code: hook preflight, §8 incomplete-decode rule, §8/§9 seed wording, the Step 0 reference name, the kit-B smoke, the reboot-safe cap count, the laptop chain and the monitoring rule (§1.2 item 6).

## 14. Open questions for the judge

1. **Q1 incomplete seeds:** ≥ 2 complete seeds for a P-B1 verdict, a seed with any missing level leaves the fit (§7.4). Ken proposed it; W11 is silent. Confirm, or rule that one complete seed gives S5's single-seed verdict.
2. **Q2 scoring venv:** kit B in `/root/vsps/.venv` (S5's venv) rather than C's `/root/venv-c1score` (`4b81b6b6…`). The kit files are sha-pinned either way; confirm.
3. **Q3 L1/L2 sft.jsonl sha256:** recorded write-once at the M3 build, before any training, rather than pinned now (pinning now needs `build_gold_sft.py` run on the laptop over KTVIC captions, as the S5 author did). Confirm, or require a laptop build before commit.
4. **Q4 Step 0 adapter:** Step 0 uses the n2 `p1dev_s42` adapter (uploaded, `227a3312…`), which is not one of the 15 points. Confirm it stays (0.06 GPU-h; it tests M3's decode path against a registered decode).
5. **Q5 lock visibility:** `cen_fetch.no_pilot` sees only `grl_pilot/RUNNING`, not `b1_scaling/RUNNING`; C-EN is kept out by the tmux rule of `cen_chain.sh`. Should `no_pilot` be amended to refuse any `/root/outputs/*/RUNNING` (a C-EN amendment)?
6. **Q6 F1 matched count:** Ken's matched-prefix count-controlled F1 is not adopted; F1 and CHAIR_i are reported as S5 computed them. Confirm.
7. **Q7 failed-step policy:** any non-timeout GPU failure is a JOB STOP to the judge (no automatic retry); Ken proposed one rerun after a NaN loss. Confirm.
8. **Q8 laptop chain:** ruled by CC-128 W9; written as `scripts/b1_scaling/b1_chain.sh` (dry-run / stage / run / cleanup); it still needs a judge code read and the gatekeeper commit before the first M3 run.
9. **Q9 file size:** `b1.py` exceeds aislop's 400-line guideline (warning, not fixed); splitting it would add pinned files.
