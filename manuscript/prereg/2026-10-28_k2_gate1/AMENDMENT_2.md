# K2 Gate 1 rule, amendment 2 (DRAFT): resume on M1 (role m3) after the M3 loss

**Status:** DRAFT v6 (final hardening round), 2026-10-29. Its threat model is MT4 `AMENDMENT_1_DRAFT.md` A0: code covers an honest operator choosing after seeing results, partial resumes, host loss, and late or partial freezes; deliberate tampering (clock setting, hand-written JSON, force-push) is left to the audit trail, and branch protection on q2 `main` is requested from the PI. `check` runs on the laptop only; M1 never gets `gh` credentials. Applies the Codex round-4 push-receipt check and CC-162 W2–W8 (W6 is the separate `AMENDMENT_2a_DRAFT.md`), CC-162a F1, F4 and F5, the Codex re-read (93) items (a) and (c), CC-162b G1, and the Codex round-3 decision anchor. Written before any Gate 1 decode of val 924 and before any `gate1_decide.json`. No Gate 1 score exists, so no look has been taken (RULE §7, CC-135). It binds only after a one-judge diff read and the gatekeeper's commit, as `AMENDMENT_2.md` with its sha in both `SHA256SUMS` copies (CC-162 W7). Its irreversible parts (`NOT_AFTER`, the exit-6 rule) are in the CC-162 W1 package with `2026-10-28_mt4_kv/AMENDMENT_1_DRAFT.md` and need the PI's answer and a Codex read; until that package is committed no K2 file is restored to M1 and the job stays HELD (CC-162 decision).

**Sources:**
- CC-160 ruling 2 and W3–W6; CC-162 rulings 1–10 and W2–W8, and its Codex review;
- PI-1029h, which answers CC-160 Q1 YES (un-park MT4/K2 and resume Gate 1 with all four arms on M1 after A's P50) and Q2 (a panel rules any KV-freeze re-pin before any Gate 1 or KV output);
- OPS-1029a (M3 lost) and OPS-1029d (M1 setup with `WITH_K2=0`);
- RULE §5, §6, §8 and the Amendments section; amendment 1 (`w25_excluded_ids.txt`, f4da5ff9).

**What it changes:**
- the ledger (one closing line);
- the lock;
- `NOT_AFTER`;
- the machine and `EXPECT_HEAD`;
- the job guards: every GPU attempt starts from zero (its decode partial is deleted first); each ledger line is fsynced before the step runs; an open ledger start is charged its full logged timeout and then faults (exit 6); no decision is written at or after `NOT_AFTER`, checked by the single locked writer at the write itself; the job refuses to run while PASCAL-50S is staged, and a reused manifest must match the restaged image shas.

**What it does not change:** any arm, threshold, SESOI, trainer, decode path, scorer, gold, caps, the Gate 1 total of 36 GPU-h, or the decision rule. It is a schedule, ledger and machine amendment. Measured rates are not added (the caps were already fixed by `caps.json` on M3).

## 1. What happened

- The job ran on M3 at HEAD f4da5ff9. It started at 2026-10-28T13:13Z.
- These steps finished with matching `.done` files: teacher, detect, targets (CPU), timing, caps (CPU), train_unedited and train_gold.
- train_det started at epoch 1793207506 (2026-10-28T17:11:46Z). M3's rental then expired. The last good backup is from 17:54Z, when `train_det.log` showed 2500 of 4784 steps.
- No `adapters/det` directory exists in the backup, so there is no orphan to delete (RULE §6).
- train_ref and all five val-924 decodes never started. `gate1_decide.json` does not exist.
- Backup: `.session_backup/machines/M3/root/outputs/k2_gate1/`. Every `.done` file was re-verified there on 2026-10-29 with `sha256sum -c` and all are OK. Only shas and counts were read; no prediction, target or log content was opened (CC-135).

## 2. (a) Closing the open ledger line

- The backup ledger (`gpu_seconds.tsv`, sha 5133c498…) ends with the open line `train_det start 1793207506`.
- `k2_gate1.used_seconds` charges an open start up to the current time. A literal restore would therefore charge more than 36 h, `left` would return 0, and job l.101 would write `gate1_decide.json` as NOT-RUN (cost). That closes the gate for good (CC-160 "What was checked").
- **Rule:** the restored ledger gets exactly one appended line, `train_det 6120`. This charges 1.7 GPU-h, the train_det stage cap in `caps.json`.
- That cap is a hard upper bound, not an estimate. The step ran under `timeout` = min(1.7 h cap, total left) = 6,120 s, so it could not have used more.
- The real elapsed time was **between 0.71 and 0.86 h**: `backup.log` shows the last contact (rc 23) at 17:54:25Z and the first rc 255 at 18:03:19Z, and the mtime of `train_det.log` is 17:36Z (CC-162 W5). The panel chose the cap over that range (CC-160: J2 and J3, with J1 accepting it as the conservative choice).
- After the append the ledger sha is **377efca0d840e1f4ccadc3185df5f23f44f0041f57d6828b2a35e7e002858b66**, pinned in `amendment2_restore.sha256`.
- The re-run of train_det adds its own `train_det start` and `train_det SECONDS` lines. The 1.7 h already charged for the lost attempt is **not** refunded.
- **Standing rule (CC-162 W8, ruling 3; Codex review):** every GPU step logs its timeout at its start, `NAME start EPOCH TIMEOUT`, where TIMEOUT = min(stage cap, Gate 1 total left). An open start is charged that **full logged timeout**, whatever the cause (host lost, job killed) and whatever the clock says.
  - `k2_gate1.used_seconds` charges an open start with a logged timeout exactly that timeout.
  - Before any retry, `k2_gate1.left` finds the open start, appends `NAME TIMEOUT` (the full charge) to the ledger, and exits 6. The job turns exit 6 into NOT-RUN (fault), which is rerunnable (RULE §7).
  - The rerun then sees a closed ledger and gets min(cap, total left). If the charge has spent the total, `left` returns 0 and the job's existing cost stop writes `gate1_decide.json` as NOT-RUN (cost). Losing a host can therefore never lower the charged cost or dodge the cost stop.
  - A legacy open start without a logged timeout (written before this amendment, as the M3 line) exits 6 **without** any write and is closed only by a committed amendment. Its timeout is determined, not chosen: `train_det` = min(1.7 h, 36 h − 3.96 h) = 6,120 s, which is the line above.
  - **Every attempt starts from zero (CC-162a F1):** before a GPU step without a matching `.done`, the job runs `k2_gate1.py fresh` on that step's decode partial (teacher, timing and the five val decodes) and logs the deletion. Without it, a kill shortly before the timeout would turn a would-be exit 124 (NOT-RUN (cost)) into a fault, and the retry would finish the remaining slices on a fresh cap. With it, a step longer than its cap ends in exit 124 however often it is killed. Training already has no resume (`cmd_train` refuses an existing adapter).
  - **A step whose child exits with a code** (a crash, or a kill of the child) still writes its measured seconds (the job's end line) and is a fault, as RULE §7 says. CC-162a ruling 4: with F1 in place, a full charge would add no protection and would only burn slack on an honest crash. A pure open start (no end line) is still charged its full timeout.
  - **Durable start record (Codex (c)):** start and end lines are written by `k2_gate1.py ledger`, which writes, flushes and fsyncs the file and its directory before the job launches the step.
  - Selftests prove it:
    - a host lost twice in the same step costs 2 × the timeout, and the charge does not depend on the clock;
    - a charge that exhausts the total gives `left` = 0, the cost stop;
    - a legacy open start writes nothing;
    - a killed child is charged its measured 42 s;
    - a start line is fsynced for the file and the directory;
    - `kill_rerun_selftest`, with the real `decode_hf_vlm.decode_slices`, shows that a step needing 5 slices under a cap of 3, killed after 2, finishes on a resumed retry (the loophole) and hits its cap on a `fresh` retry.
  - Exit 6 as a rerunnable fault changes which MT4 branch binds when a host is lost (MT4 PREREG §0 row 3), so it is ruled inside the W1 package (CC-162 ruling 3), not by this reversible amendment.

## 3. (b) The stale lock

- `RUNNING` in the backup (sha a19d7803…, written 2026-10-28T13:13:06Z by the M3 job) is **not restored**.
- Its sha and the reason are written as one line in `runs.log` and in WORKFLOW_LOG at restore time.
- setup_gpu.sh already excludes `*/RUNNING` (l.73).

## 4. (c) Arms and reuse

All four trained arms stay: unedited, gold, det and ref (RULE §3). Dropping det or ref is not proposed (CC-160 ruling 2).

| Step | Reused? | Pinned sha (output) |
|---|---|---|
| teacher | yes, `teacher.done` | `k2g1_qwen3vl_8b_ut-detailed.preds.json` 9f3c2690… |
| detect | yes, `detect.done` | `detect.json` 03acf723… |
| targets (CPU, no `.done`) | yes, file present | `targets.json` d25473f2…, `targets.json.counts.json` beae71e2… |
| timing | yes, `timing.done` | `k2g1_timing.preds.json` dfb6bce9… |
| caps (CPU, no `.done`) | yes, file present | `caps.json` 5fc76d97… (cap total 30.0, fits) |
| train_unedited | yes, `train_unedited.done` | adapter **056b92cc**…, `train.json` 4fac4f65… |
| train_gold | yes, `train_gold.done` | adapter **055a9793**…, `train.json` 6b279088… |
| train_det | **rerun from scratch**, seed 0, same config | no adapter exists |
| train_ref | run | — |
| decode × 5 (base_s, unedited, gold, det, ref) | run, all on M1 | — |
| decide | run once | — |

- The manifests `ut.tsv` (a532eca8…), `probe.tsv` (def9511d…) and `reg_teacher.json` (428be13f…) are reused as files, since the job rebuilds them only when they are missing.
- Each sha above is checked by `amendment2_restore.sha256` before the job starts (§8).
- The adapter shas 055a9793 and 056b92cc match CC-160.

## 5. (d) NOT_AFTER and run order

- **New `NOT_AFTER` = 2026-11-10T12:00:00Z** (epoch 1794312000, `k2_gate1.NOT_AFTER`), the value of the W1 package (CC-162 ruling 2 (a); MT4 `AMENDMENT_1_DRAFT.md`). `CLEANUP_H` = 2.0 h stays, so the last GPU step must end by 11-10T10:00Z. **Irreversible; needs the PI** (CC-162 Part B).
- **Why this date:** P50 is nearly done. The M1 mirror (`.session_backup/machines/M1/root/outputs/p50/gpu_seconds.tsv`, LOG OPS-1029g-op) keeps 7 models (14 full runs): 10 of 14 full runs were done at 03:25Z on 10-29 (start 00:51Z), 2.26 GPU-h used including 0.27 h of smoke, and the worst-case decode end at the caps is about 07:30Z on 10-29 (CC-162a ruling 5, F4). Its 11-16T12:00Z cutoff is a legal bound, not an expected end (CC-162 W2). Even if P50 used its whole 8 GPU-h cap, about 11 days would remain for about 19 GPU-h of Gate 1 (Codex review).
- **At the `NOT_AFTER` instant (new code):** a GPU step that would end after `NOT_AFTER` − 2 h is HELD (exit 4, unchanged). The job also refuses to start the decide step at or after `NOT_AFTER` (`k2_gate1.py deadline`, exit 4). The check that binds is at the write (CC-162a F5; Codex (a)):
  - `gate1_decide.py` is the only writer of `gate1_decide.json`, for both the decision and NOT-RUN (cost);
  - it holds a `flock` on `.gate1_decide.lock`, refuses at or past `NOT_AFTER`, records `written_epoch`, writes a fsynced temporary file, checks the clock again and only then renames;
  - if that second check fails, the verdict markdown just written is deleted (CC-162b G1);
  - `gate1_decide.py check` accepts a decision only if all three hold: its `written_epoch` is before `NOT_AFTER`; its sha256 is the first sha ever written to `manuscript/prereg/2026-10-28_k2_gate1/gate1_decide.sha256` on q2 `main`; and GitHub's server receipt time of a push carrying that commit (activity API, events API as the fallback) is before `NOT_AFTER`. If the API is unreachable, `check` exits 4 (HELD): it is rerun, and nothing is decided by the outage (MT4 amendment 1 A1). MT4 reads the decision only through `check`.
- **Anchoring step (operator, well before `NOT_AFTER`):** after the decide step, copy the sha of `gate1_decide.json` (`sha256sum`, never its content) into the anchor file. The gatekeeper commits it on `paper-v10` and pushes `paper-v10` to q2 `main`, and the operator logs the push output line in WORKFLOW_LOG (a record only; GitHub's receipt time is what `check` reads). A decision without such a push received before `NOT_AFTER` is no decision: Branch K1+K6.
- **Run order on M1 (CC-162 ruling 8; overtakes CC-160 ruling 3 item 1, "setup first"):**
  1. P50 decided (`p50_decide.json`);
  2. P50 data deletion logged;
  3. M1 `/root/outputs` backed up;
  4. the gatekeeper's commit of the W1 package + this amendment + amendment 2a if needed;
  5. `setup_gpu.sh` with `WITH_K2=1` (its ff-merge to the commit is the logged HEAD move);
  6. the §8 restore;
  7. the Gate 1 resume;
  8. cleanup.
- Setup and the resume never run while the `p50` tmux session, a `RUNNING` lock or P50 staging exists (setup l.286 refuses on a lock).
- The option "K2 before P50 if it provably ends before the PASCAL-50S staging" is **not** used.
- **Machine check (new):** the job refuses to start while `/root/ncs-data/datasets/pascal50s` or `/root/ncs-data/p50_raw` exists. This enforces RULE §5 ("M3 never holds test images while Gate 1 runs") for P50, beside the existing `b2_stage` check. P50's cleanup deletes both (`p50_job.sh` l.52–54).
- **KV freeze:** set by MT4 amendment 1 (Branch K2 freezes at the `KV_PRED_SUMS` commit or at D = 2026-11-30T12:00Z, whichever is first). The CC-160 option "(ii) the §8 cost-only amendment sets the K2 freeze" is withdrawn (CC-162 ruling 2: rejected 3/3).
- **Expected timing:** setup about 1 h, restore and staging about 1 h, then about 19 GPU-h of projected Gate 1 work. With P50 ending about 10-30, Gate 1 ends about 11-01 to 11-02.
- **M1 rate check (CC-162 ruling 9, recommended, not in this draft's code):** a fault-only probe outside the Gate 1 ledger (≤ 0.25 GPU-h, dev line, caps never change); HELD → PI if M1 is more than 15% slower than M3 or above 8.50 s/img. It needs its own short rule; PI question Q3 of CC-162.

## 6. (e) HEAD, machine and hardware

- **`EXPECT_HEAD`** = the gatekeeper's commit that holds this amendment, the re-pinned `SHA256SUMS` (both copies) and `amendment2_restore.sha256`, or a later commit that changes nothing in `scripts/k2_gate1/`, `scripts/grl/`, `scripts/w22_sft/`, `scripts/lb/` or the two prereg folders.
  - A HEAD change is a logged rerun that reuses every `.done`-matched step (RULE header).
  - The new `EXPECT_HEAD` and the job sha (8e288401…, was 3e604ac7…) are written to `runs.log` and WORKFLOW_LOG at start.
  - M1's clone moves to the amendment commit (a logged HEAD move) only after P50's data deletion is logged, never while P50 runs.
- **Machine:** M1, with `/root/.vsps_machine_id` = `m3` (PI-1029d; CC-155 W1). The job's `GPU=m3` check, the machine-id check and `k2_gate1.guard` (`K.host_ok` = m3) are unchanged. M4 and M2 (role m4) stay refused.
- **Hardware change (disclosed):** M1 is a different physical host from M3. It is a newly rented NVIDIA RTX 3090 (24 GB), running Ubuntu 22.04 with driver 580.126.18, the same driver as M3.
  - Its software was rebuilt from the pinned freezes by `setup_gpu.sh` (sha e68b8532…). The OPS-1029d run used `WITH_K2=0`, so venv-q3, venv-gd, the GD weights and the K2 checks are not on M1 yet.
  - Train and decode are not bit-reproducible across hosts (bf16, NF4 and cuDNN nondeterminism; MT4 PREREG §3).
  - The gating contrasts G1–G4 compare K (gold) with base_s and U (unedited). K and U were both trained on M3, and all five val decodes run on M1 on the one student path. G1–G4 are therefore within-host for training and within-host for decoding.
  - **K vs det and K vs ref are cross-host training contrasts** (K on M3; det and ref on M1). They feed only secondaries (H-P2r dev, matched-count F1 K vs ref), never a gate, and are labelled cross-host in `gate1_decide.json`'s report (CC-162 W7).
  - The `train.json` of the M3 arms records the old job sha, and the M1 arms record the new one.
- **Cap risk (disclosed):** `caps.json` was fixed from M3's timing probe (6.89 s/img base path; worst case 8.50). If M1 is slower, a step can hit its cap. Exit 124 is NOT-RUN (cost) under the unchanged RULE §7, which closes the gate. No re-probe is allowed, because that would change a cap after training began.
- **Setup with `WITH_K2=1` (CC-160 W4):**
  - Before setup runs, one judge reads the diff of the `WITH_K2` path of `setup_gpu.sh` (e68b8532; ll.15, 52–54, 118, 219–222, 227–271, 289–299, 324, 376–378, 411–425).
  - Setup must reproduce venv-q3 **2bb7397e**, venv-lb **685ffe2a** and venv-gd **5291fc30**, plus `snapcheck` (14 B-N1 files) and the C-EN records that `common.guard` needs (§8 step 3).
- **If venv-gd does not reproduce 5291fc30:** setup_gpu.sh l.264 stops ("ruling needed") and the job's freeze loop would FAULT → PI; there is no rebuild-and-go. CC-162 ruling 4 chose option (i): **amendment 2a** (`AMENDMENT_2a_DRAFT.md`, pre-written, filled only after setup prints the new hash) re-pins `H_GD` at job l.14 and setup l.54 together, adds RULE l.49 and l.126 to the superseded list, re-pins SUMS, gets a one-judge read, and is followed by a full setup rerun. The detector output is reused only by its `.done` sha. Option (ii), skipping the gd checks, is rejected.
- If venv-q3 or venv-lb does not reproduce, it is FAULT → PI with no option, because both feed remaining steps.

## 7. (f) Corrected K2 numbers

| Item | GPU-h |
|---|---|
| Closed ledger on M3: teacher 7,718 + detect 512 + timing 287 + train_unedited 2,876 + train_gold 2,857 s | **3.96** |
| train_det charge (this amendment) | 1.70 |
| **Charged before the resume** | **5.66** |
| Remaining caps: train_det 1.7 + train_ref 8.0 + decode base_s 2.3 + 4 × 2.8 | 23.2 |
| Worst case at the caps: 5.66 + 23.2 | 28.86 ≤ 36 |
| Remaining projection (`caps.json`): 1.41 + 6.66 + 1.87 + 4 × 2.28 | **≈ 19.1** |
| Expected Gate 1 total | ≈ 24.7 |

- The CC-160 statement "~4–5.7 GPU-h used, ~19 to finish" is confirmed: 3.96 h measured, 5.66 h charged, and 19.1 h projected.
- The portfolio figures of "17 GPU-h spent" and "3–6 to finish" are wrong (CC-160 W6). The portfolio owner fixes that text, not this rule.
- The dev line (40 GPU-h) is unchanged.

## 8. (g) Restore procedure on M1 (operator; counts and shas only)

Never `cat`, `head`, `less` or `jq` a prediction, target, partial or log file. The only reads are `sha256sum`, `wc -l`, `ls` and `test`.

1. **Preconditions:**
   - the run order of §5 steps 1–5 is done: P50 decided, its deletion logged, M1 outputs backed up, the W1 package and this amendment (and 2a if needed) committed, setup with `WITH_K2=1` finished with every pin matched (§6);
   - no `/root/ncs-data/datasets/pascal50s` and no `/root/ncs-data/p50_raw`;
   - no `/root/outputs/*/RUNNING`, no tmux session, and the GPU is idle.
2. Confirm that `/root/outputs/k2_gate1` does not exist on M1. If it exists, stop and refer to the PI.
3. **C-EN records (CC-162 W3, W4):** the six C-EN test-side hash/id records (CC-157 l.24–26) are **already on M1** with the pinned shas: done.json 6b3c4d75…, fc4c2942…, e19eb75e…; sha256.tsv 614afa1b…, 8c93f306…, fbbcd21c…. Setup (`WITH_K2=1`, l.290–291) and this step only verify them; nothing is copied. They are held only on the m3 role, as `common.guard` refusal lists, never on M2 or M4. A mismatch is a FAULT → PI.
4. **Copy** the files listed in `manuscript/prereg/2026-10-28_k2_gate1/amendment2_restore.sha256` (paths relative to `/root/outputs`) from the local backup to M1 with `rsync`, file list only. These are:
   - the reused step outputs and their `.done` / `.sha256` / `.log` files;
   - `ut.tsv`, `probe.tsv`, `reg_teacher.json`, `targets.json`, its counts file and `caps.json`;
   - both adapter folders;
   - `runs.log`;
   - `gpu_seconds.tsv`;
   - the Gate 0 bf16 val decode `grl_pilot/k2/k2g0_qwen3vl_8b_val-detailed.preds.json` (8bb0192c), the RULE §2 diagnostic row (CC-162 ruling 6: restore).
5. **Not copied:** `RUNNING` (§3), `train_det.log` (the partial log of the lost attempt, which stays in the backup), and every `*.partial.jsonl` (the reused steps' final files are present, so decode resume never needs them).
6. **Close the ledger:** `echo "train_det 6120" >> /root/outputs/k2_gate1/gpu_seconds.tsv`.
7. **Verify:**
   - `cd /root/outputs && sha256sum -c /root/vsps/manuscript/prereg/2026-10-28_k2_gate1/amendment2_restore.sha256` must report 32 of 32 OK;
   - then `cd k2_gate1 && for f in *.done; do sha256sum -c "$f"; done` must report 7 of 7 OK;
   - and `test ! -e adapters/det` must hold.
   - Any mismatch is a FAULT → PI. Nothing is repaired by hand.
8. **Staging:** the job stages UT-2402 + val 924 itself (`common.stage`; M1 has no `images.sha256`). The operator places the two pinned release files in `$UV/src` first, as on M3.
   - **Code check (new):** right after staging, the job runs `k2_gate1.py stagecheck` on the reused `ut.tsv` (2,392 rows) and `probe.tsv` (40 rows). It compares column 3 with the staged `images.sha256` and prints only the mismatch count. Exit 7 is a FAULT → PI, before any GPU step.
   - Reason: the reused teacher output and targets must belong to the same images that det and ref train on.
   - Val is pinned by `stage()` against `uitviic_val.tsv`.
9. **Log:** append one line to `runs.log` and one to WORKFLOW_LOG with the restore result (32/32, 7/7), the `RUNNING` sha excluded, the ledger close, the new `EXPECT_HEAD` and the job sha. Then start the job: `EXPECT_HEAD=<commit> GPU=m3 bash scripts/k2_gate1/k2_gate1_job.sh` in tmux.
10. **First-run expectation:** `stagecheck` reports 0 of 2,392 and 0 of 40; then teacher, detect, timing, train_unedited and train_gold log "reused (sha matches), no GPU step", and train_det starts with `left` = 6,120 s.

## 9. Code changes (selftests rc 0 on the laptop, 2026-10-29)

**`scripts/k2_gate1/k2_gate1.py`** (6a4fe404… → 2fda9603…):
- `NOT_AFTER` = 1794312000 (2026-11-10T12:00Z). The HELD message is derived from the constant.
- The ledger:
  - start lines carry the logged timeout;
  - `used_seconds` charges an open start its full logged timeout;
  - `open_start` returns the last line when it is a start;
  - `left` closes such a start at its full timeout and exits 6, or exits 6 without a write for a legacy start (§2).
- New `ledger_append` / `ledger` command (fsync of the file and the directory) and `fresh` / `fresh` command (delete a step's decode partial).
- New `deadline` command (exit 4 at or after `NOT_AFTER`).
- New `stage_mismatch` and the `stagecheck --manifest` command (exit 7 when a manifest image is missing or differs from the staged sha).
- Selftests:
  - `ledger_selftest`: fsync count, the killed child's measured charge, the open-start charge at any clock, 2 × the timeout for two losses, `left` = 0 when the charge spends the total, a legacy start refused, and the amended M3 ledger (20,370 s, 5.66 + 23.2 ≤ 36 h);
  - `kill_rerun_selftest` (F1, §2);
  - `stage_mismatch`.

**`scripts/k2_gate1/gate1_decide.py`** (14fbbd16… → f3312447…):
- `records` holds the `flock` and refuses at or past `NOT_AFTER`, then records `written_epoch`;
- `write` fsyncs the temporary file and re-checks the clock before the rename;
- `check` also re-runs the decision on its recorded input shas and requires an identical result (round 6; `rerun_selftest`: a hand-edited verdict and a changed input sha are refused);
- new `check` command: the first-anchor rule on `refs/remotes/q2/main`, and GitHub's push receipt time read through `gh api` (activity API, events API as the fallback; only the head sha and the timestamp). It exits 4 (HELD) when the API is unreachable;
- on a refusal at the rename, the verdict markdown is deleted (G1);
- `deadline_selftest` covers a late direct `decide` and cost `notrun`, the race across the instant (no json and no markdown left), the lock, and a forged or missing `written_epoch`.
- `anchor_selftest` uses a temporary repository with a bare remote and a mocked GitHub push record (no network). It accepts a push received before `NOT_AFTER`, also through a descendant head. It refuses a backdated commit pushed late, a missing push, an unknown head, a forged unanchored decision and a second decision anchored later, and it HOLDs (exit 4) when the API is down.

**`scripts/mt4_kv/kv_freeze.py`** (new, 56439faf…, pinned in `mt4_kv/SHA256SUMS`): the KV freeze writer and validator of MT4 amendment 1 A3/A4 (CC-160 W9). It touches no KV data.
- `NOT_AFTER` is imported from `k2_gate1`, so there is one constant.

**`scripts/k2_gate1/k2_gate1_job.sh`** (3e604ac7… → 5ddce0ed…):
- `step NAME CAPS PARTIAL -- cmd`: `fresh` on PARTIAL before the start line;
- start and end lines go through `k2_gate1.py ledger` (fsynced);
- each start line logs the step's timeout;
- left exit 6 becomes NOT-RUN (fault, rerunnable after the full charge);
- the decide step is refused at or after `NOT_AFTER`;
- the HELD message no longer names 11-06 or N9;
- the job refuses to start while PASCAL-50S staging exists;
- `stagecheck` runs on `ut.tsv` and `probe.tsv` after staging, when they exist;
- the job selftest fails unless all three decode steps pass a partial.

**Re-pins:**
- `SHA256SUMS`, both copies, are re-pinned and identical (70a213b3…).
- RULE.md and every other pinned file are unchanged.
- At the commit, the gatekeeper adds this file's sha and the sha of `amendment2_restore.sha256` to both copies (as for amendment 1).

**RULE.md lines this amendment overrides (RULE.md bytes unchanged; a diff reader should read them as superseded):**
- l.34, l.54 and l.108–110, "M3 only" / "it is used only where it exists (M3)": now the m3 role, which is M1 (`/root/.vsps_machine_id` = m3). The guard is unchanged. The same reading applies to the job's comment at l.161 ("the diagnostic row exists on M3 only").
- l.111, the run order: replaced by §5 above.
- l.112, `NOT_AFTER` 2026-11-06T12:00Z (N9 start): now 2026-11-10T12:00Z, and no decision at or after it.
- l.113, "PASCAL-50S uses M3 from 11-08": P50 runs first on M1, and Gate 1 runs after P50's data deletion.
- l.144–145, the ledger: start lines log the timeout; an open start is charged its full logged timeout and then faults (exit 6), §2. The b1 "charged up to the next start" rule applies only to legacy lines.
- l.167 (RULE §7, NOT-RUN (fault)): adds "an open ledger start, after it is charged its full logged timeout" and "the decide step at or after `NOT_AFTER`" (HELD).
- MT4 PREREG §0, §2, §8 and §9: changed only by MT4 `AMENDMENT_1_DRAFT.md` (W1). PREREG.md bytes do not change.

## 10. MT4 PREREG

- `PREREG.md` is **byte-unchanged** (dd0fe943…). It is the HOLD file and is pinned in three `SHA256SUMS`. There is no verifier arm and no VI–EN contrast (CC-160 W6).
- The HallE-Control distinction (arXiv 2310.01779) is added as row 21 of `2026-10-28_mt4_kv/PRIOR_ART_W23.md`, the prior-art file that PREREG l.11 relies on. `mt4_kv/SHA256SUMS` is re-pinned.
  - **Honest overlap:** HallE-Control also uses COCO ground truth (through the RAM tagger) to decide which objects a caption target keeps, so "gold-informed targets" is not unique to K2.
  - **What remains:** a deterministic deletion of clauses from the training backbone's own captions, plain SFT of that backbone, an unedited self-training control, the truncation frontier at matched recall, and Vietnamese.
  - The narrowed "setting novelty" sentence (PREREG l.11) still holds, and the 80% pivot rule is not triggered.
  - Row 21 rests on an automated summary of the HTML. A full-text read is required before any KV-side reliance or any setting-novelty sentence, and the bracketing claim stays marked unverified until then (CC-162 ruling 10, W11).

## 11. Disclosures added to the Gate 1 report (RULE §10)

- Gate 1 ran on two hosts. Teacher, detect, timing and the K and U arms ran on M3; the det and ref arms and all five val decodes ran on M1 (same GPU model and driver; venvs rebuilt from the pinned freezes). M3 was lost mid-train_det and the det arm was retrained from scratch. G1–G4 are within-host; K vs det and K vs ref are cross-host training contrasts.
- 1.7 GPU-h was charged for the lost det attempt, which is the cap, against between 0.71 and 0.86 h elapsed (backup.log: rc 23 at 17:54:25Z, first rc 255 at 18:03:19Z; train_det.log mtime 17:36Z). Stated in RULE §10 and the supplement.
- `NOT_AFTER` was moved from 11-06 to 11-10 by amendment 2 and MT4 amendment 1, before any val decode.
- Caps came from M3's timing probe and were not re-measured on M1.
- [Only if amendment 2a applies] venv-gd was rebuilt with a different freeze sha. The detector output had been produced on M3 with 5291fc30 and was reused by sha.

## 12. Rulings applied and what is still open

- **Ruled by CC-162:** Q1 option (ii) rejected (ruling 2); Q3 option (i), amendment 2a (ruling 4); Q4 the C-EN records are test-side lists held on the m3 role only (ruling 5); Q5 restore (ruling 6); Q6 disclose 0.71–0.86 h (ruling 7).
- **Open, in the W1 package for the PI and Codex (irreversible):**
  - **Q1.** `NOT_AFTER` 2026-11-10T12:00Z and the Branch K2 freeze rule (MT4 `AMENDMENT_1_DRAFT.md`). Default if not answered: K2 stays HELD after P50 and the current PREREG text binds.
  - **Q2.** The exit-6 rule of §2, now with F1 (every attempt from zero) and the fsynced start line. CC-162a sub-question for the PI: should a step killed with an exit code be charged its measured seconds, provided every retry restarts from zero? Rec: YES. Default: YES (implemented). If F1 is refused, charge the full timeout.
- **Open, PI (reversible):** CC-162 Q3, the M1 rate check (§5). Q4, A's freeze is 12-18 at SPIC.

