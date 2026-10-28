# K2 Gate 1 dev gate rule: a Qwen3-VL-8B student trained on its own gold-edited captions, against base, unedited and truncation controls (val 924)

**Status:** written 2026-10-28, before any Gate 1 output; v2 applies CC-151 W2–W9 and PI-1026bb. No teacher decode of the training pool, no adapter and no Gate 1 score exist. The rule binds once the gatekeeper commits it together with `scripts/k2_gate1/`, after the 3-judge read (CC-148 W1, CC-151) and the one-judge diff read of v2.

**EXPECT_HEAD (CC-151 W6).** `EXPECT_HEAD` is the latest commit that holds this rule, its W25 amendment (`w25_excluded_ids.txt`) and the conditional MT4 PREREG. The W25 amendment and the PREREG move HEAD after the rule commit. Each HEAD change is a logged rerun (`runs.log` and WORKFLOW_LOG) that reuses every finished step whose `.done` sha file matches; no output is read in between.

**Scope:** this rule covers only the Gate 1 dev gate on UIT-ViIC val 924. The conditional MT4 confirmatory PREREG is `manuscript/prereg/2026-10-28_mt4_kv/PREREG.md` (KV-4,224, H1–H3, seeds 3/3/2/2, English arm). It holds both branches: the K2 arm binds on a Gate 1 GO, the K1 + K6 headline on a NO-GO (PI-1026bb Q1). **It is committed before ANY Gate 1 GPU step, teacher decode and training included** (CC-148 r1 read literally; CC-151 r1). This rule licenses nothing on KV.

**Sources:**
- CC-148 W1–W15 and ruling 1;
- PI-1026av (all CC-148 defaults);
- PI-1026bb (CC-151 Q1–Q3): the MT4 PREREG before any Gate 1 GPU step; Gate 1 on M3 only; MT4 cap **170 GPU-h** = test 100 (confirmatory seeds and KV decodes) + dev 40 + English 30. It replaces PI-1026aw's 160;
- CC-151 rulings 1–13 and W2–W9;
- PI-1026ax and CC-150a (M3 kept);
- OPS-1028u (W22-SFT PASS on C1);
- CC-119 W1–W5 and W9–W13, W19–W21, W25;
- K2_GATE0_RULE §2, §5, §6b and §6c.

**Drafts:**
- This rule finalizes Ken's `manuscript/ken/K22_K2_GATE1_RULE_DRAFT.md` (sha c1bd0912).
- Ken's `K22_W22_SFT_AMENDMENT_DRAFT.md` is **superseded**: W22-SFT is done (`manuscript/prereg/2026-10-28_w22_sft/PREREG.md`, OPS-1028t-op).

**Label:** DEV / NOT A METHOD RESULT. A GO only activates the K2 branch of the already-committed MT4 PREREG and licenses the confirmatory training. Gate 1 adapters are never test systems (PILOT_RULE §6).

## 1. Authority

| Source | What it fixes here |
|---|---|
| CC-148 W3, W4 | the arms; fixed 2 epochs, last checkpoint, no dev grid |
| CC-148 W5 | the GO conditions and their thresholds |
| CC-148 W7 | one pinned student decode path, with the base re-decoded on it |
| CC-148 W9 (= CC-119 W25) | the HOLD until the pHash/SSCD near-duplicate pass is done |
| CC-148 W11 + PI-1026bb Q3 | stage caps of ceil(1.2 × projection), inside the 40 GPU-h MT4 dev envelope |
| CC-151 r2 + PI-1026bb Q2 | the machine: **M3 only**, overruling CC-148 W12 and CC-150a for Gate 1 dev only (§5) |
| CC-148 W13 | the disclosures (§10) |
| CC-119 W1, W3–W5, W20, W21 | SESOI −3.0 CHAIR_i and −2.0 recall, 512 tokens, the 90% words rule, the editor, the scorer and the gold. None of these is reopened |
| CC-119 W12 | GO on one-seed point estimates, with CIs reported (§7) |
| W22-SFT PREREG §2, §5 | the trainer config. "The Gate 1 trainer uses that config verbatim": C1, i.e. `w22_sft.load(snapshot, gc=False)` |
| K2_GATE0_RULE §5 (CC-124 W2) | the two STOP classes: NOT-RUN (cost or fault) is never a negative pilot |

## 2. Fixed now

| Item | Value |
|---|---|
| SESOI | CHAIR_i −3.0, recall margin −2.0 (CC-119 W1; `k2_gate0.G`) |
| Backbone | `Qwen/Qwen3-VL-8B-Instruct` @ `0c351dd01ed87e9c1b53cbc748cba10e6187ff3b`, with 14 files checked against B-N1 (sha 9ff02dc2) by `w22_sft.py snapcheck` before any GPU step. The 7B fallback (PI-1026av Q3) is not needed: W22-SFT passed on 8B C1 (OPS-1028u). Ken's §9 and question 7 are moot |
| Teacher (target source) | the Gate 0 decode path unchanged: `scripts/lb/decode_hf_vlm.py`, venv-lb (freeze 685ffe2a), bf16, sdpa, batch 4, greedy, `min_pixels` 262,144, `max_pixels` 1,048,576, `PROMPTS["detailed"]` (sha 0addb5dd), `max_new_tokens` 512. The registration is `k2_gate0.registration` with the data set swapped to the UT pool (`k2_gate1.teacher_reg`) |
| Editor | `k2_gate0.untruncate` and `k2_gate0.edit` (matcher v1, language check, final-punctuation rule), imported, not copied |
| Detector (det arm) | `k2_p2_detect.load_detector`, `class_scores`, `present`, `BOX_T` = 0.30 (K2_GATE0_RULE §6c.1–§6c.3), run on the UT pool in venv-gd (freeze 5291fc30) |
| Trainer (every trained arm) | `w22_sft.load(snapshot, gc=False)` verbatim: QLoRA NF4 with double quant and bf16 compute, sdpa, LoRA seed 0, r 16, α 32, dropout 0, language tower only (43,646,976 trainable parameters, asserted inside `load`). AdamW at lr 1e-4 (`w22_sft.LR`), weight decay 0, constant lr, no warmup, no clipping. 8 micro-batches of 1 per optimiser step (`w22_sft.ACCUM` = `common.CFG["sft_examples_per_step"]`, which answers Ken's question 4). The last partial group takes one step. Loss uses the `labels=` path with −100 over the prompt and `use_cache=False`. Exactly **2 epochs; the last checkpoint is kept; no grid** (CC-148 W4, J2 default). Example order: `train.schedule(sorted keys, 2 × n, 0)` |
| Seed | one seed (0) per arm (CC-148 ruling 1). Seeds 3/3/2/2 belong to the MT4 PREREG only |
| Student decode path (W7) | `k2_gate1.student`:<br>- `w22_sft.load()` gives the 4-bit NF4 base plus a fresh LoRA;<br>- the arm's saved adapter state is loaded into it with `set_peft_model_state_dict` (504 LoRA tensors asserted, no unexpected key);<br>- then eval mode, KV cache on and left padding.<br>Decoding uses `decode_hf_vlm.make_generate` / `decode_slices` / `write_output`: greedy, 512 new tokens, batch 4, the same prompt and `max_pixels`, in venv-q3 (freeze 2bb7397e). No merge |
| Base on the student path | **base_s** = the same loaded net with its fresh LoRA left in place. `lora_B` = 0 is asserted, so the update is exactly zero and the base runs the identical path, LoRA compute included. It is decoded by the same code and is the comparator of every GO condition |
| bf16 base row | Gate 0's val decode (sha 8bb0192c…0c51), labelled "shared with Gate 0 (W7)". It is a diagnostic only, never a comparator, and it is used only where it exists (M3). CC-151 r5 |
| Scorer (W20, W21) | `k2_gate0.row` / `rates`:<br>- matcher v2;<br>- negated or hedged mentions count as hallucinations, never as TPs;<br>- CHAIR_i = Σhal / Σmen × 100 (pooled);<br>- R = Σtp / Σ\|gold\| × 100;<br>- gold = `gold_instances.json` (sha 42c100f5).<br>Every decode is passed through `untruncate` before scoring (W3, all rows). Paired image bootstrap: B = 2,000, `default_rng(0)`, one draw shared by every system |
| Frontier (G4) | `k2_gate0.p1_frontier` on the **base_s** captions, cut to the first k clauses (`units`), interpolated at R(K). Only its gap, CI and clamp flag are used. Its own 6.0 threshold (`p1_gap_min`) is Gate 0's and plays no part here |
| Noun-phrase guard (CC-119 W13) | `score_dev.caption_row(...)["noncoco"]`: `rescap.chair.objects_in` (pinned e47d249a) on the text left after the v2 class spans are blanked. Frozen now and **reported** for every system. It does not gate (CC-151 r10) |
| Language check (G6) | a caption fails if it contains a character matched by `clean_supervision.CJK_RE` or `OUT_OF_SCRIPT_RE` (sha 01f17200), the editor's own check (`k2_gate0.language_ok`). The share is per caption. The per-character share is reported beside it (CC-151 r3) |

## 3. Arms and the training mix (CC-148 W3; CC-119 W10, W11)

Every trained arm starts from the same base and the same fresh LoRA (seed 0), with the same prompt and the same §2 config, on the post-W25 pool. The arms differ in their target text and, through the empty-target rule below, in which pool images they keep (disclosed, CC-151 r9).

| Arm | Training text | Role |
|---|---|---|
| **base_s** | none; base decoded on the student path | comparator of G1, G2 and G4 |
| base_bf16 | none; Gate 0's decode | diagnostic only |
| **unedited** (SFT-unedited) | the teacher caption after `untruncate`, unedited, one per image | G3: the mechanism control (W10) |
| **gold** (K2 gold-edited, "K") | `edit(caption, gold)`, one per image | **the gated arm** |
| det (K2 detector-edited) | `edit(caption, D(img) at 0.30)`, one per image | H-P2r dev numbers only (P2 licence, §6c.5); never gates |
| ref (SFT-ref, not K1) | every human reference of the pool images (12,012 for UT-2,402), 2 epochs | reference row; matched-count F1 against K (reported) |

G-RL is not an arm of this rule (CC-148 ruling 1). It has its own rule and cap.

**Training mix (CC-151 r11).**
- The unedited, gold and det arms each train on **exactly one detailed target per image and no human reference**. Their ratio is 1 : 0.
- Human references appear only in the ref arm.
- This is an **explicit, disclosed overrule of CC-119 W11** ("plus human short references"), ruled by CC-151 r11. It is not a reading of CC-148 W3, which is a hyperparameter list. Reason: mixing references into the K2 arms would make K2 minus unedited a mixed contrast.

**Empty targets.**
- An edited target with no units left drops that image from that arm. Nothing is substituted.
- The number dropped per arm is reported in `targets.json.counts.json`, with the staged `train_data.json` sha (the `common.stage` cut, so not the release pin) and the reference count (CC-151 W5).
- An image with no reference drops from the ref arm.
- Accepted, report-only (CC-151 r9). **Disclosed:** dropped images make the K and U arms differ in images as well as in text.

**Long targets.**
- The teacher stops at 512 new tokens, and `untruncate` and `edit` only remove text. Re-tokenising the decoded text can still differ by a few tokens.
- Targets are **never truncated**.
- The trainer reports label-length percentiles per arm and the count above 512 (`train.json`, numbers only).
- W22 measured a peak of 19.30e9 B at 512 positions, which leaves 4.2e9 B of margin below the 23.5e9 limit (CC-151 r9).
- **OOM path (CC-151 r13).** A CUDA out-of-memory error in any step exits 5. The job records NOT-RUN (fault) → TO-PI. There is **never** a silent switch to the C2 config (gradient checkpointing) or to any other config; a C2 rerun needs an amendment and a ruling.

## 4. Data and isolation

- **Training pool:** UT-2,402 (`ut2402.txt`, sha 3969bfd4) **minus the ids in `w25_excluded_ids.txt`**. That file is the output of the W25 pHash/SSCD pass of UT-2,402 against KV-4,224 and OIV7 val (CC-148 W9, on M3).
  - The pass and its thresholds are their own rule, `manuscript/prereg/2026-10-28_w25_neardup/RULE.md` (`scripts/w25/`).
  - Its output is committed as amendment 1 of this rule before any Gate 1 GPU step, and its sha joins `SHA256SUMS` then. The MT4 PREREG's sha joins `SHA256SUMS` at the PREREG commit. Neither line can exist before its file is committed, so both are pinned when each file lands (CC-151 W3); until then the HOLD is the `git` check below.
  - **HOLD (CC-151 W3).** `k2_gate1.pool` and job step 1 read the W25 file and the MT4 PREREG **from the HEAD commit** (`git show HEAD:` / `git cat-file -e HEAD:`), never `is_file()`. An untracked or uncommitted copy is `HELD`; the clean-tree check ignores untracked files, so it cannot release the HOLD. The selftest covers both cases in a temporary repository.
  - The counts 2,402, 2,532 and 2,695 are reported beside the post-W25 pool (PILOT_RULE §1).
- **Dev score:** all of UIT-ViIC val 924 (`uitviic_val.tsv`, sha 338252e1). `k2_gate0.val_ids_ok` (W19) runs before every val decode and before the decision.
- **No KV image is decoded or staged** in Gate 1. UT-2,402 ∩ KV-5000 = 0 by id.
- **Timing probe:** the first 40 ids of the post-W25 pool, `pool()[:40]` (CC-151 W6), so a W25-excluded id is never decoded. These are decoded on the base_s path for the decode rate only. The rate in seconds is the only value used, and no text is read.
- **Guard (`k2_gate1.guard`, before every GPU step):** M3 only. `common.guard` runs verbatim: host, idle GPU, committed clean HEAD, `m3_clear`, no UIT-ViIC test file, and the test-image scan including the C-EN test-side shas. Any other host is REFUSED (CC-151 r2). Job step 1 also refuses while the W25 tmpfs stage `/dev/shm/w25` exists.
- Lock `/root/outputs/k2_gate1/RUNNING` (noclobber), tmux-only with exactly one session, no other `/root/outputs/*/RUNNING`, no `b2_stage`, `EXPECT_HEAD` with a clean tree, and the host id equal to `GPU=`.

## 5. Machine and window (CC-151 r2; PI-1026bb Q2)

- **M3 only**, for Gate 1 dev. This overrules CC-148 W12 and CC-150a for Gate 1 only. M4 keeps B-1, and no Gate 1 job runs on M4.
- Why M3: it is kept (PI-1026ax) and idle; it holds venv-lb, venv-gd and venv-q3, the pinned 0c351dd snapshot, the UT-2,402 + val-924 staging (3,326 images with `images.sha256`) and the bf16 diagnostic decode; W25 must run there.
- **M4 is refused** by `k2_gate1.guard` and by the job (`GPU` must be `m3`) until an amendment removes the C-EN record dependency of `val_ids_ok` / `refused_sets` (k2_gate0.py:301-311, common.py:112-122). On M4 the job would pass the old guard, spend about 17 GPU-h on the teacher and training, then FAULT at `decode_base_s`.
- **Run order on M3 (CC-151):** (0) W1 import check on M3 (operator) → rule commit → (1) the W25 rule committed and run → (2) the W25 bytes deleted and the deletion logged → (3) the conditional MT4 PREREG committed → (4) Gate 1 steps 1–8 → (5) cleanup → A's N9 rescue starts 11-06 12:00Z.
- **NOT_AFTER (CC-151 W4).** `NOT_AFTER` = 2026-11-06T12:00:00Z (N9 start). `CLEANUP_H` = 2.0 h is reserved before it for pulling the outputs, deleting the staged UT/val images and verifying. `k2_gate1.py left` exits 4 when a step's timeout would end after NOT_AFTER − 2.0 h. The job checks this **before** the ledger `start` line, so nothing is charged. It is a HELD fault, rerunnable after a ruling, and never a cost stop.
- M3 never holds test images while Gate 1 runs. PASCAL-50S uses M3 from 11-08.

## 6. Steps (`scripts/k2_gate1/k2_gate1_job.sh`)

0. **Entry conditions:**
   - W22-SFT PASS on C1 (OPS-1028u; w22_decide sha 100f7274);
   - the W1 import check ran on M3 from a scratch copy of the snapshot before the rule commit, with one OPS line of return codes (CC-151 W1, PI-1026ba);
   - this rule and its code are committed;
   - the W25 exclusion file is committed (amendment 1) and the W25 bytes' deletion is logged;
   - the conditional MT4 PREREG (`2026-10-28_mt4_kv/PREREG.md`, both branches) is committed **before any Gate 1 GPU step** (CC-151 r1, PI-1026bb Q1);
   - the machine is M3 (CC-151 r2).
1. **CPU checks, before any GPU step:**
   - both selftests and `SHA256SUMS`;
   - for venv-q3 (2bb7397e), venv-lb (685ffe2a) and venv-gd (5291fc30): the venv exists, its `pip freeze` sha equals the pin, and `pip check` is clean. No venv is built by this job;
   - `w22_sft.py snapcheck` (the 14 B-N1 pins);
   - the W25 file and the MT4 PREREG at HEAD (`git cat-file -e`), and no `/dev/shm/w25`;
   - guard;
   - **import check first:**
     - `w22_sft.py imports` in venv-q3: every W22 module and symbol, the five version pins and a GPU NF4 round trip;
     - then `k2_gate1.py imports --venv q3`: `peft.set_peft_model_state_dict`, `safetensors.torch.load_file`, `decode_hf_vlm`, `train.schedule` and `w22_sft`;
     - then `--venv gd`: `groundingdino.util.inference`, `k2_p2_detect` and CUDA.
     - Exit 3 is a FAULT before any GPU step.
2. **Teacher** (GPU, venv-lb): the decode of the pool at 512 tokens. Its sha is recorded.
3. **Detector** (GPU, venv-gd): D(img) at 0.30 on the pool. Its sha is recorded.
4. **Targets** (CPU): the unedited, gold, det and ref targets. Counts only go to stdout and `targets.json.counts.json`.
5. **Timing probe** (GPU, venv-q3): the base path (fresh zero LoRA, LoRA compute included) on the 40 probe ids. Then **caps** (CPU, `caps.json`) are fixed from the measured rate (§8). If the cap total exceeds the Gate 1 total, the result is NOT-RUN (cost) before any training.
6. **Train** (GPU, venv-q3): the unedited, gold, det and ref arms, seed 0. Each run's adapter sha and `train.json` are recorded.
7. **Decode** (GPU, venv-q3, the one student path): base_s, unedited, gold, det and ref on val 924.
8. **Decide** (CPU, `gate1_decide.py decide`): one look, which writes `gate1_decide.json`.

**How the job runs each GPU step:**
- Each step runs under `timeout` = min(its cap, the Gate 1 total minus the ledger) (`k2_gate1.py left`). `left` failing is a FAULT (`left=$(...) || fault`, CC-151 W6); its exit 4 is the NOT_AFTER HELD (§5).
- The ledger gets a `NAME start EPOCH` line before the step and a `NAME SECONDS` line after it. An open start is charged up to the next start (b1 rule), so a reboot cannot undercount.
- Output goes to `>> log 2>&1` with `rc=0; cmd || rc=$?`. There is **no `| tee` anywhere**, because a tee masked an exit code in N9. The job selftest fails if such a pipe appears.
- A step whose `.done` sha file matches its outputs is reused on a rerun without GPU work. The teacher decode and the val decodes resume from finished slices (`decode_slices`).
- A crash between an adapter or decode write and its `.done` file leaves an orphan that the step refuses to overwrite. The operator deletes that orphan output, logs the deletion in `runs.log` and WORKFLOW_LOG, and reruns. The deleted output was never read.

## 7. Decision rule (CC-148 W5; `gate1_decide.py`, selftested)

K = gold-edited student, B = base_s, U = SFT-unedited. All values are point estimates on val 924, one seed (CC-119 W12).

| | GO condition (all must hold) |
|---|---|
| G1 | CHAIR_i(K) − CHAIR_i(B) ≤ −3.0 |
| G2 | R(K) − R(B) ≥ −2.0 |
| G3 | CHAIR_i(K) − CHAIR_i(U) ≤ −3.0 |
| G4 | CHAIR_i(B's truncation frontier at R(K)) − CHAIR_i(K) ≥ 3.0 |
| G5 | mean words(K) ≥ 0.90 × mean words(B) (syllables, `rl_reward.syllables`) |
| G6 | share of K captions failing the language check ≤ 2% |

**Outcomes:**

| Outcome | When |
|---|---|
| **NOT-RUN (fault) → TO-PI** | Any of these: a setup failure, a pin, sha or freeze mismatch, a guard refusal, the W25 or PREREG HOLD, the NOT_AFTER HELD, an import-check failure, a non-finite training loss, an all-zero `lora_B` in a loaded adapter, an OOM (exit 5; no C2 switch), or a crash that is not a cap hit. It writes `GATE1_FAULT_<utc>.md` only. It is not a look, and a logged rerun is allowed while `gate1_decide.json` does not exist |
| **NOT-RUN (cost) → TO-PI** | Exit 124 of any step, or the caps after the timing probe exceeding the Gate 1 total. It writes `gate1_decide.json` + `STOP.md` and closes the gate. It is not a negative pilot |
| **NO-GO** | any of G1, G2, G3, G5, G6 fails; or G4 fails without a low clamp |
| **INCONCLUSIVE** | G1, G2, G3, G5 and G6 hold, but the frontier is **clamped low**: R(K) < R_1, the recall of B cut to its first clause, so there is no equal-recall comparison (CC-125). The clamp can only block a GO. It never loosens a gate. In practice it is nearly unreachable, because R_1 ≤ R(B) and G2 needs R(K) ≥ R(B) − 2 |
| **GO** | G1–G6 all hold, with no low clamp |

**High clamp (CC-151 r4).**
- When R(K) > R_max, the uncut recall of B, no truncation of B reaches K's recall. `k2_gate0.interp` then uses the endpoint, so the G4 gap equals CHAIR_i(B) − CHAIR_i(K), which is −G1.
- K beats the whole frontier in that case. The rule reads G4 at the endpoint, flags `frontier_clamped_high`, and does **not** call it INCONCLUSIVE.
- CC-125 was written for Gate 0, where edits only delete and an edited caption can never exceed the zero-shot recall. Only the low clamp could arise there.
- A student can exceed base_s's recall, for example because it learned from bf16 teacher captions while base_s is NF4. Treating that as INCONCLUSIVE would block exactly the best outcome.

**Default on Ken's half-width rule.** CC-119 W12 sets GO on point estimates with CIs reported. Ken's extra INCONCLUSIVE on bootstrap half-widths (draft §6 (b)) is therefore **not adopted**. Every half-width is reported (CC-151 r10).

**One look.** The look is the moment `gate1_decide.json` is written. After it there is no rerun, no hyperparameter change, no extra seed and no other checkpoint.

**Branches:**
- **NO-GO** writes `STOP.md`. K2 is a disclosed negative dev pilot, with no KV look for K2. The NO-GO branch of the committed MT4 PREREG binds: the headline is K1 + K6 (PI-1026u Q4; PI-1026av Q1), and the UPGRADE_PLAN §6 pivot review follows.
- **INCONCLUSIVE** goes to the PI. There is no second val look. The only route without a second look is K2 entering KV as a descriptive arm with no H, which needs a new ruling.
- **GO** activates the K2 branch of the committed MT4 PREREG and licenses the confirmatory seeds. It is not reported as a finding. Measured Gate 1 rates may enter the PREREG only as a cost-only amendment (CC-151 r1).

## 8. Caps (CC-148 W11, PI-1026bb Q3) and the W4 length count

**Measured inputs:**
- W22-SFT C1 (w22_decide 100f7274): s_ex_512 = **0.7892 s**, s_ex_64 = 0.454 s, peak 19,304,284,160 B.
- Gate 0 val decode (gate0_decide 0b6da7e0): **3.25 s/img** bf16 over the whole run, the CC-148 anchor of 3.24.
- P2 detector (p2_decide 837ada55): **0.2089 s/img**.
- Student NF4 + PEFT decode rate: **not measured yet**. The timing probe (§6 step 5) measures s_probe on the base path before any training.
  - The base_s decode cap uses s_probe.
  - The four trained-arm decode caps use the worst case `s_worst = s_probe × 512 / k2_gate0.slice_steps(probe rows, 512, 4)`. This is Gate 0's freeze scaling: every slice runs to the 512-token cap, because a trained student may decode longer than the base. It applies to the four arms only.

**Formula (`k2_gate1.plan`):**
- Stage projection (GPU-h) = work / 3600 + 0.1 load. Stage cap = ceil(1.2 × projection) to 0.1 GPU-h.
- teacher = n_pool × 3.25.
- detect = n_pool × 0.2089.
- timing = 40 × 3.25 × 2.0, the planning factor.
- each of unedited, gold and det = 2 × n_pool × 0.7892 × 1.25.
- ref = 2 × n_refs × 0.7892 × 1.25.
- decode base_s = 924 × s_probe; each of the 4 trained-arm decodes = 924 × s_worst.
- The **1.25 CPU allowance** covers preprocessing, which the W22 rates exclude (W22 PREREG §9; CC-151 r7).
- **SFT-ref is priced at the 512-token rate**, a guaranteed upper bound (see W4 below). The 64-token figure is shown beside it (CC-151 r8).

**Planning numbers at the full pool (2,402 images, 12,012 references):**

| Stage | Projection | Cap |
|---|---|---|
| teacher | 2.27 | 2.8 |
| detect | 0.24 | 0.3 |
| timing probe | 0.17 | 0.3 |
| train unedited / gold / det (each) | 1.42 | 1.7 |
| train ref (512 rate) | 6.68 | 8.1 |
| decode × 5 at 3.25 s/img (bf16 rate, s_worst = s_probe) | 0.93 each | 1.2 each |
| decode × 5 at 6.5 s/img (2× bf16, the planning factor, s_worst = s_probe) | 1.77 each | 2.2 each |
| decode base_s at 6.5, 4 arms at s_worst 8.3 | 1.77 / 2.23 each | 2.2 / 2.7 each |
| **Total** at 3.25 / 6.5 / 6.5 + 8.3 | 18.28 / 22.45 / 24.30 | 22.6 / 27.6 / 29.6 |

At the 64-token rate, SFT-ref would project 3.89 GPU-h (cap 4.7) instead of 6.68.

**Budget lines (PI-1026bb Q3; CC-151 r6):**

| Line | GPU-h | Holds |
|---|---|---|
| dev | 40 | Gate 1 36 + W22-SFT 0.75 (used 64 s) + W25 3.25 (wall cap of its job) |
| test | 100 | the confirmatory seed training (about 30 GPU-h, seeds 3/3/2/2) **and** the KV-4,224 decodes (MT4 PREREG) |
| English | 30 | the English arm (MT4 PREREG) |
| **MT4 total** | **170** | PI-1026bb Q3; replaces PI-1026aw's 160 and PI-1026av's 115 |

**Gate 1 total = 36 GPU-h:**
- The total is enforced by the job, and the sum of caps must fit under it.
- With s_probe = 6.5, the caps stay inside 36 while s_worst ≤ about 13.5 s/img. Above that, the result is NOT-RUN (cost) before training, the cheap place to fail.
- **Correction (CC-151 r6).** CC-150 r1 read the confirmatory seeds as part of dev 40. That reading is corrected: dev 40 holds only Gate 1, W22 and W25, and the seeds sit on the test line. The interim "Gate 1 dev 20" of CC-148 W11 (also the W22 PASS line) is replaced by this split.

**CC-150 W4 length count (count-only; no caption text printed or stored):**
- Source: the 12,012 UIT-ViIC training references of the UT-2,402 ids, from the release train file. Its sha 441d22d2 equals `common.SRC_PINS["train_data.json"]`.
- The images carry 1, 5, 9 or 10 references each.
- The Qwen3-VL-8B tokenizer **could not be loaded locally**: only `tokenizer_config.json` is cached and transformers is not installed on the laptop. The documented proxy is therefore used: syllables (`rl_reward.syllables`, whitespace split after `.,;:!?`).

| Measure | mean | p50 | p90 | p95 | p99 | p99.9 | max |
|---|---|---|---|---|---|---|---|
| syllables | 12.16 | 12 | 15 | 16 | 18 | 23 | 31 |
| whitespace words | 13.12 | 13 | 16 | 17 | 20 | 24 | 31 |
| UTF-8 bytes | 74.1 | 73 | 90 | 97 | 110 | 139 | 179 |

**Reading:**
- Syllables are not Qwen tokens, since one Vietnamese syllable can be several BPE tokens. The proxy therefore does not prove that every reference fits in 64 label positions.
- 64 positions hold the p99 reference (18 syllables) if the tokenizer uses ≤ 3.5 tokens per syllable, and the longest (31 syllables) if it uses ≤ 2.0.
- The only hard bound is UTF-8 bytes, because a byte-level BPE gives at most one token per byte. The longest reference is 179 bytes, so it needs at most 180 label positions with `<|im_end|>`, below the 512 measured by W22.
- Hence SFT-ref is priced at s_ex_512, a guaranteed bound. The trainer records the real per-arm label-length percentiles (`train.json`) as the token-level answer.

## 9. Reported in `gate1_decide.json` (numbers and shas only)

- Per system (base_s, unedited, gold, det, ref, and base_bf16 where present):
  - CHAIR_i, R, and the Gate 0 diagnostics (unasserted-excluded, negation-blind, union-gold);
  - Σhal, Σmen, Σtp, Σ|gold|;
  - mean words;
  - language-check caption share and out-of-script character share;
  - non-COCO nouns per caption (W13);
  - cap-hit share and s/img.
- G1–G4 deltas with bootstrap half-widths and the frontier gap's 95% CI.
- Frontier points by k, the clamp flag, and check T (truncation of B meeting G1 as written).
- **Registered secondaries, never gating:**
  - matched-count F1 (Paper A's matched prefix, cited as a tool) for K vs base_s and K vs ref;
  - H-P2r dev: R(K) − R(det) and CHAIR_i(K) − CHAIR_i(det);
  - ceiling retention = (CHAIR_i(B) − CHAIR_i(K)) / (9.375 − 1.7948), with the NF4 numerator and bf16 denominator stated.
- The lexicon-evasion share is defined in the MT4 PREREG, not here.
- The shas of every decode and adapter, `caps.json`, the target counts, and the label "DEV / NOT A METHOD RESULT".

## 10. Disclosures (CC-148 W13; Gate 0 §7)

- Paper A's matched-count estimator is cited as a measurement tool. MT4 makes no count-control claim.
- **Val 924 reuse:**
  - It served as B's WiSE-FT gate, for B adapter decodes, as G-RL dev, and at Gate 0, P1, P2 and now Gate 1.
  - All 924 are COCO train2014 images and may be in pretraining data.
- **Training side:**
  - 88 UT-2,402 ids were touched by Paper A, and 857 are restval (also in C-EN memory).
  - These are training-side facts, not test exposure.
- COCO-80 only: every claim covers those 80 classes.
- No Vietnamese references exist on KV, so there is no test CIDEr. Gate 1 itself scores val, which has references.
- The detector (GD-T) may have seen Visual Genome images (§6c.2). If so, the det arm benefits.
- K2 training text is the backbone's own captions, edited against gold. It is training data, not evidence: no machine-translated COCO and no AI-silver labels (PI-1026aa Q5; no new gold labels).
- The comparator is the NF4 base on the student path, with the bf16 row beside it.
- **Language filter in the targets (CC-151 W9).** The gold and det editors delete every unit that fails the language check (`k2_gate0.edit`, l.79). G6 for K, and partly G3, therefore reflect that training-side filter as well as anything the student learned.
- **Arms differ in images (CC-151 r9).** An empty edited target drops that image from that arm, so K and U can train on slightly different image sets; the counts are reported.
- **Training pool.** UT-2,402 minus the W25 near-duplicates of KV-5,000 and OIV7 val (W25 RULE); 2,402, 2,532 and 2,695 are reported beside it.
- This rule's cap figures rest on measured rates, except the student decode rate, which is measured by the timing probe before training.

## 11. Pre-written report sentences (filled from `gate1_decide.json`)

- **GO:** "On UIT-ViIC val (924 images), a Qwen3-VL-8B student fine-tuned with 4-bit QLoRA for two epochs (last checkpoint, no tuning) on its own detailed captions after deterministic gold-based clause deletion lowered CHAIR_i by X points relative to the same-precision base model, with object recall changing by Y points, and by Z points relative to a student trained on the unedited captions; it stayed W points below the base model's clause-truncation frontier at equal recall [high clamp: its recall exceeded every truncation of the base, so the frontier comparison reduces to the base comparison]. All pre-set development thresholds (−3.0 CHAIR_i, −2.0 recall, 90% length, ≤ 2% captions failing the language check) were met; this licensed the confirmatory test and is not itself a result."
- **NO-GO:** "On the development set, the gold-edited student did not meet the pre-registered gate (failed: …; ΔCHAIR_i X, Δrecall Y, gap to the truncation frontier W). Per the rule, K2 was not run on the test set; it is reported as a negative development pilot, and the paper's headline rests on K1 + K6."
- **INCONCLUSIVE:** "The development gate could not be resolved: the student's recall fell outside the base model's truncation frontier, so no equal-recall comparison existed. No second development look was taken; the decision was referred to the PI."
- **NOT-RUN (cost):** "Step … exceeded its pre-registered cap of P GPU-h (or the stage caps exceeded the 36 GPU-h Gate 1 total). Per the rule this is a cost outcome, not a negative result; no gate decision exists."
- **NOT-RUN (fault):** "The pinned pipeline could not be run as registered (reason: …). No substitute configuration was tried."
- **Every outcome:** "Development used UIT-ViIC val (924 COCO train2014 images, used in earlier pilots of this project) and the UIT-ViIC training images minus near-duplicates of the test images; scoring covers the 80 COCO classes only, with COCO-2014 instance annotations as gold."

## 12. Rulings of CC-151 (formerly judge items J1–J13)

- **J1 order (r1).** The conditional MT4 PREREG is committed before ANY Gate 1 GPU step (PI-1026bb Q1). Ken's "after GO" condition is struck. A GO activates its K2 branch.
- **J2 machine (r2).** M3 only; M4 refused (§5; PI-1026bb Q2).
- **J3 G6 unit (r3).** Per caption, with the per-character share reported beside it. The stakes, corrected: the bf16 base was 95.67% `vietnamese_only` at Gate 0, a broader test that also requires diacritics. The base's `language_ok` share is **unmeasured**, so how close a 2% caption-level gate sits to the base's own rate is not known.
- **J4 / J4b (r4).** Frontier from base_s. Low clamp INCONCLUSIVE; high clamp reads G4 at the endpoint and is flagged (§7).
- **J5 (r5).** Gate 0's bf16 val decode is reused as a labelled diagnostic; CC-148 W7's ban applies to KV.
- **J6 (r6).** Gate 1 total 36 inside dev 40; seeds on the test line (§8).
- **J7 (r7).** CPU allowance 1.25 accepted.
- **J8 (r8).** SFT-ref priced at the 512 rate accepted.
- **J9 (r9).** Target rules accepted, report-only, with the image-difference disclosure (§3, §10).
- **J10 / J11 (r10).** Ken's half-width INCONCLUSIVE not adopted; the noun-phrase guard stays report-only.
- **J12 (r11).** 1:0 mix as an explicit, disclosed overrule of CC-119 W11 (§3).
- **J13 (r12).** HOLD mechanics with the tracked-at-HEAD check (§4). W25's procedure is its own rule.
- **OOM (r13).** NOT-RUN (fault), TO-PI, never a silent C2 switch; a cost stop stays NOT-RUN (cost).

## 13. Not decided here

- The MT4 PREREG content (`2026-10-28_mt4_kv/PREREG.md`): KV-4,224 freeze about 11-18, H1–H3 fixed sequence, seeds 3/3/2/2, the English arm, lexicon evasion, and the test cap (100 GPU-h, PI-1026bb Q3).
- Venue: IP&M VSI MMLowRes, SJR (PI-1026ay); NCA dropped (PI-1026aw, CC-149). CC-119 W23 (novelty) and W26 (venue check) bind the MT4 PREREG commit, not this dev rule.
- The 7B fallback: moot after OPS-1028u.

## Amendments

- **Amendment 1 (reserved, CC-148 W9 / CC-151 r12).** `w25_excluded_ids.txt` (the W25 output, possibly empty) is added to this folder and its sha to `SHA256SUMS`, by the gatekeeper, after the W25 run and the logged byte deletion. The text of this rule does not change.
- **PREREG pin (reserved, CC-151 W3).** At the MT4 PREREG commit the gatekeeper adds the sha of `manuscript/prereg/2026-10-28_mt4_kv/PREREG.md` to both copies of `SHA256SUMS`.
- A later cost-only amendment may replace planning rates with measured ones; it changes no gate, threshold or arm.
