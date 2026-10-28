# Pre-registration addendum: N9 rescue, a base-only fidelity fix (dated 2026-10-28, append-only)

**Status.** Written 2026-10-28, before any rescue decode. No N9 method output has ever been scored or read. The gatekeeper commits this file after a judge read and before attempt 1 starts (CC-142 W1: by 10-31).
**Parent registration.** `2026-10-18_n9_count_matched_leaderboard.md` / `.json` (b8b2500), with its companion `2026-10-18_e1_k2_placebo_addendum.md`. Both stay byte-identical (sha256 `7e244a48…`, `2b232bd3…`, `c6238a7c…`). This sibling file adds the fix that the parent §7 K-F calls for ("the protocol is fixed before any method look"). It changes nothing else.
**Rulings.** PD-15 item 2 (the only route back to testability: a base-only fix committed as an N9 addendum, then re-decode the base and repeat K_F, then decode every method). CC-140 ruling 3 (conditions), CC-142 W1 (joint K2/N9 batch handling, branch texts, novelty anchor, hard stop 11-08), PI-1026ao (rescue approved; novelty scored after the result), PI-1026ap (N9 on M3 10-31..11-05).
**Later amendments** to this file are appended below §10 with a date. Nothing above them is edited.

## 1. What stays as registered

- Checkpoints, pins, loading rule and expected merge counts (parent §1); images, scorer, gold, statistics, endpoints, predictions (a)-(c), every threshold and every kill rule (parent §3-§7).
- **K-F tolerances: |ΔCHAIR_i| ≤ 1.0 and |ΔCHAIR_s| ≤ 1.5, against LiM's published 15.4 / 50.0. Unchanged.**
- The code. `scripts/lvlm/decode_llava.py` (`522bfc16…`), `scripts/lvlm/e1_chair_count.py` (`1e59ff12…`) and `scripts/lvlm/score_k2_n9.py` (`b0f270c4…`) are unchanged. The scorer therefore still accepts the committed `data/results/n9_k2/e1check.json` (`f991039…`) and the K2 result `.session_backup/2026-10-18/n9k2_scoring/k2/k2_scores.json` (`0f0e952e…`, C* = matched_prefix). No rescore of K2 takes place.
- One look. The analysis plan (parent §8, steps 3-5) is unchanged: nothing from a method run is scored until every run of the attempt exists and K-protocol passes, and then it is scored once, by `score_k2_n9.py n9`.

## 2. The fix: at most two attempts, both named now, base only

**Base-only evidence behind the choice.** All of it was disclosed under PD-15 item 3.
- The 10-18 base run (`n9_base`, sha `3498648e…`, batch 8, on M2) gave CHAIR_i 13.91 and CHAIR_s 50.3 (diff −1.49 / +0.3).
- The same scorer gives 15.26 on LiM's own released r1 captions, so the gap is in decoding, not in scoring.
- Only 3.6% of base captions equal LiM's r1 caption exactly. The median first divergence falls at word 9, and mean lengths are 90.8 vs 90.3 words (`.session_backup/2026-10-19/n9_kf_disclosure/{kf_local,divergence}.json`).
- 0 of 500 base captions reached the 512-token limit; the longest has 218 new tokens (base metadata only).

**LiM's reference path, read at `yuezih/less-is-more@f26e187aadacc49a7cfc30443f0e9bae865b8e2e`** (the commit that the registered id list comes from):
- `CHAIR-eval/eval.sh` (sha256 `453664215d7629623eb1afd9cc1ba5e0738347a301ae9e12db0146a49fceb9eb`) runs `LLaVA/llava/eval/model_vqa.py` with `--temperature 0` and no other decoding flag.
- `LLaVA/llava/eval/model_vqa.py` (sha256 `45ae7d68953d1d5df365d7574fe4ed2776cb39b1a4144489ea891637541bf29a`):
  - l.41-72: one image per `generate()` call, i.e. batch size 1;
  - l.94: default conv mode `llava_v1`;
  - l.99: `num_beams` 1;
  - l.64: image tensor `.half()`; the builder loads fp16;
  - l.71: `max_new_tokens=1024`.
- `CHAIR-eval/data/chair-500.jsonl` (sha256 `d4002b20…`, the registered id source): 500 of 500 rows carry the question "Please describe this image in detail.", the same string as ours.
- So the prompt, template, dtype, greedy decoding and beam count already match. Neither side pads: our harness gives every image of a batch the same prompt ids.
- **Two stated settings differ from ours: the batch size (1 vs 8) and `max_new_tokens` (1024 vs 512).**

**Attempt 1 (runs first): batch size 1. Everything else is as registered, including 512 new tokens.** This is LiM's own setting. Rationale (CC-140 r3): a median first divergence at word 9 points to batch-dependent fp16 numerics, not to the prompt.

**Attempt 2 (only if attempt 1 fails K_F): batch size 1 and `max_new_tokens` 1024** (model_vqa.py l.71). Everything else is as registered.
- **Trigger, machine-checked and base-only.** Attempt 2 runs only if two conditions hold:
  - attempt 1's K_F verdict is FAIL;
  - at least one attempt-1 base caption has `hit_max_new_tokens` = true (`n9_rescue.py trigger2`).
- Otherwise attempt 2 is **void**. Under greedy decoding, a caption that stops before 512 tokens is the same token for token under a 1024 limit, so attempt 2 would repeat attempt 1 exactly.
- **Scoring path, fixed now.** `score_k2_n9.py` checks `max_new_tokens` against the registered 512. For attempt 2 only, `scripts/lvlm/n9_rescue.py score1024 <mode> …` imports the unchanged scorer, replaces only the expected `max_new_tokens` with 1024, and stamps the wrapper sha into the output.
- **Disclosed cost.** A 1024 run adds a second setting mismatch against K2 (512 tokens), on top of the batch size (§3).

**Not chosen:**
- A different prompt string, dtype or padding side: these already match LiM, so CC-140's examples give nothing to change.
- Swapping the software stack, which LiM's `LLaVA/pyproject.toml` pins at transformers 4.37.2 and torch 2.1.2, plus LLaVA's own model class. That is not one exact setting: it needs a new venv and a new harness.

**After the attempts.**
- If attempt 1 fails and attempt 2 is void or also fails, **N9 is final NOT-TESTABLE.** The same holds after a CAP STOP, a start-rule stop or the 11-08 hard stop (§4).
- Every failed base run is kept and disclosed: its sha, its K_F diffs, its settings and its hit_max count.

## 3. Joint K2/N9 batch registration (CC-142 W1)

**The problem.** The parent §2 (l.61) and §7 K-protocol (l.222) register one batch size for every N9 and K2 run. K2 ran at batch 8 on 10-18, and its result is known: HELD, C* = matched_prefix. LOG l.220 calls the batch size "registered jointly for K2 and N9".

**GPU-h of the two choices.**
- Anchors on M2: base 8.7 min at batch 8 (T8 = 0.145 h). K2 seed 2 took about 10 min at batch 8 (≈ 1.15 × T8).
- The batch-1 slowdown r is unknown, plausibly 3-6×, so the batch-1 base time T1 is 0.44-0.87 GPU-h. It is measured by attempt 1 and drives the cap (§4).
- The start rule (§4) needs 7·T1 ≤ 6 − T1, so a rescue is feasible only if T1 ≤ 45 min.

| Choice | Extra runs | Rescue total (base + 7 others [+ K2 pair]) | Fits the 6 GPU-h ceiling if |
|---|---|---|---|
| (i) Re-run the K2 pair at batch 1 | 2 sampled runs ≈ 2.3·T1 = 1.0-2.0 GPU-h | 10.3·T1 = 4.5-9.0 GPU-h | T1 ≤ 35 min (r ≤ 4.0) |
| **(ii) Carry C* and disclose (chosen)** | 0 | 8·T1 = 3.5-7.0 GPU-h | T1 ≤ 45 min (r ≤ 5.2) |

**Choice: (ii), carry C* = matched_prefix from the batch-8 K2, disclosed as a K-protocol deviation.** Reasons:
- **Budget.** (i) takes 1.0-2.0 GPU-h out of the same ceiling and kills the rescue for any r between 4.0 and 5.2. (ii) leaves the whole ceiling to the registered runs.
- **One look.** (i) would be a second placebo look at a test whose result is known. With fresh per-image seeds at batch 1 it could move C* by chance, after the fact (CC-140 r3).
- **What K2 measures.** K2 calibrates the paired control on two exchangeable sampling draws of one model. Batch size reaches it only through fp16 kernel numerics, which both seeds share.
- **No code change.** `score_k2_n9.py n9` checks batch equality among the eight N9 runs, all at batch 1, and reads C* from `k2_scores.json`.

**Disclosure text (Supplementary S4, and §6.4 in the scored branches):** "C* carried from batch-8 K2 against a batch-1 N9 run": the seed placebo (K2) that selected the matched prefix was decoded at batch 8 on 10-18 and was not re-run. Every N9 run of the scored attempt used batch 1{, and 1,024 new tokens against K2's 512}. This departs from the registered single batch size for K2 and N9 (prereg §2, §7 K-protocol).

## 4. GPU cap, start rule, hard stop, machine

All constants are in `scripts/lvlm/n9_rescue.py`, with a selftest.
- **Ledger.** `/root/outputs/n9_rescue/gpu_seconds.tsv` records the wall seconds of every rescue decode, model loading included. It covers both base attempts and every method run. It excludes the 10-18 M2 runs and the CPU fetch. A step with a start but no end stops the job (fail closed).
- **Ceiling.** 6 GPU-h for all N9 rescue GPU time. Each base decode runs under `timeout` equal to what is left of the 6 h.
- **Cap.** Fixed once, after the attempt's base passes K_F and before any method decode, and written to `aA/cap.json`:
  - cap = min(T_base × 8 × 1.5, 6 GPU-h − GPU time used so far);
  - T_base = the measured wall time of the passing base (all segments, if resumed);
  - "× 8" follows CC-140. Only 7 runs remain (6 methods + `n9_povid_fullmerge`), so the factor is conservative.
- **Per-run limit.** Each method run is killed at the cap remaining. A CAP STOP before or during a method run is final: N9 is NOT-TESTABLE, because `n9` mode needs every registered run.
- **Start rule.** No method decode starts, final NOT-TESTABLE (`START_RULE_STOP.json`), if either holds:
  - the projected need 7 × T_base exceeds the cap;
  - the projected finish, now + cap, is after **2026-11-06T12:00:00Z**.
- **Hard stop: 2026-11-08T12:00:00Z.** CC-142 gives the date; the hour is set here. No rescue stage starts after it. If the scored `n9` output is not on the laptop by then, N9 is final NOT-TESTABLE.
- **Machine and order.**
  - M3 only.
  - The job runs after B-2's cleanup is done and never displaces B-2 or B-1.
  - It refuses to start while `/root/ncs-data/b2_stage` exists, while any other `/root/outputs/*/RUNNING` lock exists, or while any GPU process is running. It holds `/root/outputs/n9_rescue/RUNNING` from staging to cleanup.
  - It is never concurrent with a test decode or a `--stage` step.
  - Queue: B-2 → N9 → P2 → PASCAL-50S (CC-142 W8).

## 5. Procedure (`scripts/lvlm/n9_rescue_job.sh`, M3, `/root/vsps`, tmux `n9`)

One lock, `/root/outputs/n9_rescue/RUNNING`, is held from `stage` to `cleanup`, so no other M3 job runs while the CHAIR-500 images are on M3. No COCO caption or annotation file goes to M3: K_F runs on the laptop.

- **0. Operator inventory, before staging (CC-140 W2), names and sizes only.**
  - `/root/outputs/n9_rescue/`, `/root/ncs-data/n9_stage/`, the HF cache entries of the nine pins, and free disk (the snapshots need about 60 GB).
  - `venv-lb`'s `hf` and `.venv` must use the same HF cache.
  - Any `n9_*` or `k2_*` file on M3. Such a file is not opened. Its name and size are reported and it is moved aside unread.
- **1. Stage.** `stage - <HEAD>`, CPU and online, not charged to the cap.
  - It refuses on any other lock, a B-2 stage or a GPU process, and then takes the lock.
  - It fetches the nine pinned snapshots.
  - It fetches the 500 CHAIR-500 val2014 images into `/root/ncs-data/n9_stage/images` by file name from the COCO image server and checks them against `data/coco_probe/chair500_val2014.sha256`.
- **2. Base.** `base 1 <HEAD>` decodes `n9_base` into `/root/outputs/n9_rescue/a1/` at batch 1. The operator then:
  - pulls `a1/n9_base.json`;
  - runs K_F on the laptop on the base alone: `python3 -E -P scripts/lvlm/score_k2_n9.py kf --coco-zip <annotations_trainval2014.zip, 031296bb…> --runs <a1> --e1check data/results/n9_k2/e1check.json --lim-r1 .session_backup/2026-10-18/n9k2_scoring/inputs/r1-llava1.5-7b.jsonl (f8fdd4dc…) --out <a1>/kf.json`. The output is one line and an exit code, base-only, as CC-021b;
  - puts `kf.json` back in `a1/`.
  - If K_F passes, step 3 follows.
  - If it fails, `base 2 <HEAD>` runs only when the §2 trigger holds (its K_F then goes through `n9_rescue.py score1024 kf …`). Otherwise N9 is final NOT-TESTABLE.
- **3. Methods.** `methods A <HEAD>`:
  - it requires a K_F PASS on `aA/n9_base.json` from the unchanged scorer (`n9_rescue.py kfok`);
  - it fixes the cap and applies the start rule;
  - it decodes the seven other runs of parent §1 in parent order into `aA/`, with the parent's flags, batch 1 and the attempt's token limit;
  - it writes `aA/SHA256SUMS`.
- **4. Cleanup.** `cleanup <reason> <HEAD>` removes `/root/ncs-data/n9_stage`, checks that it is gone and releases the lock. It also runs after any final stop.
- **Every stage first checks:**
  - HEAD equals the expected commit, and the tree is clean;
  - `scripts/lvlm/SHA256SUMS` verifies, which covers this file, the parent pair, the K2 addendum, the three unchanged scripts, the helper, the job, the id list, the image manifest and `e1check.json`.
  - The decode stages also check: the `.venv` freeze equals `setup_gpu.sh` H_VS; the image bytes match the manifest; `decode_llava.py --selftest` passes.
- **5. Scoring, on the laptop, once**, after `aA/` is pulled and its SUMS verifies:
  `python3 -E -P scripts/lvlm/score_k2_n9.py n9 --coco-zip <031296bb…> --runs <aA> --k2 .session_backup/2026-10-18/n9k2_scoring/k2/k2_scores.json (0f0e952e…; scored by score_k2_n9.py b0f270c4, per n9k2_scoring/ws.sha256) --e1check data/results/n9_k2/e1check.json --lim-r1 <r1-llava1.5-7b.jsonl, f8fdd4dc…> --out n9.json`. For attempt 2 the command starts with `n9_rescue.py score1024 n9 …`.
  - No method file is opened, CHAIR-checked or summarised before this one run.
  - The 30-minute backup pull of `/root` will also copy `/root/outputs/n9_rescue/` to the laptop mirror. Those mirror copies are unread too. Scoring uses only the pulled directory, after its SUMS check.
  - A K-protocol failure follows parent §7: the run is invalid, it is re-run before scoring if the cap and the dates allow, and the failure is disclosed.

**Open before staging (judge).** 128 of the 500 CHAIR-500 images are in C-EN's test-side image records: 67 in Karpathy test and 61 in Karpathy val, 0 in nocaps val. This is a count of sha256 matches between `data/coco_probe/chair500_val2014.sha256` and the M3 mirror of `/root/outputs/c_en/fetch/{coco_test,coco_kval,nocaps_val}.sha256.tsv`, through `scripts/grl/common.cen_test_shas`.
- The overlap follows from the design: CHAIR-500 and both Karpathy splits are drawn from val2014. N9 decodes them for evaluation only; nothing trains on them.
- The job keeps them on M3 only under the N9 lock and deletes them at cleanup.
- Whether that suffices, or N9 must run elsewhere, is for the judge. The 128 images are not dropped: dropping them would change the registered image set.

**Real method output on a mirror (CC-140 W2).** The laptop mirror of M2 holds one real 10-18 method decode: `.session_backup/machines/O-2308428/root/outputs/results/n9_leaderboard/n9_povid.json` (sidecar sha256 `47df1345103b8bf08a80d7aed6897be2b38ddb8072864e526ec23fb2e9994553`), with its `.partial.jsonl`.
- It was made under the failed protocol and is superseded by the rescue re-decode. It stays unread and is never scored, compared or used.
- Its file keys, label and created/finished stamps were printed on 10-28 to check whether it was synthetic. No prediction field was printed.
- The other local `n9_povid*` copies (`.session_backup/2026-10-18/n9k2_scoring/{dryrun,synth_backup,synth_backup_bad}/`) carry `created_utc` = "synthetic".

## 6. Deviations from the parent, disclosed in Supplementary S4 whichever way N9 falls

1. Batch size 1 for every N9 run of the scored attempt (registered: 8).
2. C* carried from the batch-8 K2 (§3).
3. Attempt 2 only: 1,024 new tokens (registered: 512), scored through the `score1024` wrapper.
4. M3 instead of M2. The software is the `.venv` of `setup_gpu.sh` H_VS, and each output records its own stack.
5. The failed 10-18 base and every failed rescue base, with sha, diffs and settings.
6. The base K_F was checked more than once (up to three base runs in all). It is a gate on the harness and its tolerances did not move, but the repeat is disclosed.
7. The 10-18 batch-8 `n9_povid` decode (M2 mirror, sidecar sha `47df1345…`) exists, was never scored and is unread (CC-146: the scoring run needs all 8 runs and never ran); it was decoded under the failed protocol and is superseded by the rescue re-decode. No script, agent or scan opens it (CC-146 W2).

## 7. Direction-neutral novelty anchor (PI-1026ao: scored after the result, by the panel)

- **Fixed now, before data.** N9 can affect the novelty cell only through one fact: whether the registered count-matched test of released checkpoints was carried out as registered and reported under its registered labels.
- **A scored branch is the same for novelty whichever way it falls.** Whether (b) is HELD, NOT_SHOWN or KILLED, however many methods SURVIVE, and whether K-headline triggers or not, the novelty cell receives the same treatment. The direction may enter only the evidence and application cells, under the scorecard's own anchors.
- **In the not-testable branch, N9 adds nothing to novelty.** The cell is scored as if N9 did not exist.
- **No credit is pre-committed here.** The panel gives the score after the result and cites this anchor.

## 8. Branch texts, written before any rescue data exists

Each `{…}` slot is filled from `n9.json` (or `kf.json`) by its key, with a `<!-- src -->` comment. Nothing else changes. Labels are the scorer's own:
- (b): `prediction_b.primary.verdict` ∈ {HELD, NOT_SHOWN, KILLED}. NOT_SHOWN and KILLED are the parent's NOT_HELD, and KILLED is the K-b case;
- P1: `table.*.P1.label` = SURVIVES;
- `K_headline.verdict`;
- `prediction_a.verdict`;
- `K_rank.verdict`.

### Branch S-H: N9 scored, prediction (b) HELD

- **§6.4 heading:** "6.4 Training-based methods: a registered leaderboard"
- **§6.4 paragraph 1:**
  - Trained methods' outputs are not released, so the registered checkpoint leaderboard decodes public LLaVA-1.5-7B checkpoints and their base model on the 500 CHAIR images (greedy, one beam, fp16).
  - Its first fidelity check failed: at batch 8 the harness missed the published base CHAIR_i by more than the registered tolerance (|ΔCHAIR_i| = 1.49 > 1.0).
  - A base-only fix, registered before any method was decoded under it, set the batch size to 1{; attempt 2 also raised the token limit to 1,024}. The base then met both tolerances (ΔCHAIR_i = {K_F.diff.CHAIR_i}, ΔCHAIR_s = {K_F.diff.CHAIR_s}), and every checkpoint was decoded and scored once.
  - The seed placebo that selected the matched prefix (Section 6.3) was decoded at batch 8 and not re-run; this deviation is disclosed (Supplementary S4).
- **§6.4 paragraph 2 (S-H):** Prediction (b), the primary one, held. The checkpoints trained on chosen-fewer data lowered their object count more than POVID: D_b = {est} [{ci95}] classes per caption, against a registered +0.3 with a lower bound above 0.
- **§6.4 paragraph 3 (both scored branches):**
  - At matched count (primary control: the matched prefix), {K_headline.n_survive} of six checkpoints gain at least 1.0 precision point with Holm-adjusted p < 0.05 (P1). The headline rule {did | did not} trigger.
  - Prediction (a) is {prediction_a.verdict} (median {median}, lower bound {ci95_lower}, against {comparator}).
  - {n_off} of six lie off the base's truncation frontier (P2).
  - The count-matched ranking {shows {n} significant reversals of the raw ranking | is consistent with the raw ranking, and no claim rests on it}.
  - Raw CHAIR, ΔP and Δm stand beside these in Table {N9}, never as the headline. {hit_max_new_tokens total} captions reached the token limit.
- **Table 1, A23:** `| A23 | Count-matched checkpoint leaderboard, predictions (a)–(c) (N9) | registered; base-only fix registered before method decodes | (b) **HELD**; (a) {verdict}; (c) not testable | 6.4 |`
- **Abstract, last sentence (20 words, abstract 237 ≤ 240):** "After a registered base-only harness fix, a count-matched leaderboard of six public checkpoints was scored, and its primary prediction held."
- **§8.4, second half:** "The second half did not fire: the leaderboard links training-data count sign to output count (Section 6.4)."
- **Dependent sentences to align:** sec11 "No count-control result is confirmatory" becomes "One count-control result is confirmatory, the registered leaderboard (Section 6.4)", with the rest of the sentence kept. The cover letter's leaderboard clause follows the abstract.

### Branch S-N: N9 scored, prediction (b) NOT_SHOWN or KILLED

- **§6.4 heading and paragraphs 1 and 3:** as S-H.
- **§6.4 paragraph 2 (S-N):** Prediction (b), the primary one, did not hold: D_b = {est} [{ci95}] classes per caption, against a registered +0.3 with a lower bound above 0. {KILLED only: below 0.1, its withdrawal rule fired, and the leaderboard shows no link from training-data count sign to output count.}
- **Table 1, A23:** `| A23 | Count-matched checkpoint leaderboard, predictions (a)–(c) (N9) | registered; base-only fix registered before method decodes | (b) **NOT HELD**{; withdrawal rule fired}; (a) {verdict}; (c) not testable | 6.4 |`
- **Abstract, last sentence (22 words, abstract 239 ≤ 240):** "After a registered base-only harness fix, a count-matched leaderboard of six public checkpoints was scored, and its primary prediction did not hold."
- **§8.4, second half:**
  - KILLED: "The second half also fired (Section 6.4), so both halves of the rule are met."
  - NOT_SHOWN: "The second half did not fire (D_b = {est}, above 0.1; Section 6.4)."
- **Dependent sentences:** as S-H.

### Branch NT: N9 not testable

The causes are: K_F failed on attempt 1 with attempt 2 void, K_F failed on both attempts, the start rule or a cap stop fired, or the hard stop passed.

- **§6.4 heading:** unchanged, "(not scored)".
- **§6.4 paragraph 1:**
  - Trained methods' outputs are not released, so the registered checkpoint leaderboard decodes public LLaVA-1.5-7B checkpoints and their base model on the 500 CHAIR images (greedy, one beam, 512 new tokens, fp16).
  - Its fidelity check failed: the decode harness did not reproduce the published base CHAIR_i within the registered tolerance (|ΔCHAIR_i| = 1.49 > 1.0 at batch 8).
  - A base-only fix registered before any method decode (batch size 1{; then a 1,024-token limit}) {did not pass the same check (ΔCHAIR_i = {diff}) | could not be completed within the registered GPU cap and dates}, so the leaderboard was not scored.
  - Base-only descriptives are in Supplementary S3. No method output was scored or read.
- **§6.4 paragraph 2:** unchanged.
- **Table 1, A23:** `| A23 | Count-matched checkpoint leaderboard, predictions (a)–(c) (N9) | registered | NOT TESTABLE: fidelity check failed{, also after a registered base-only fix | ; registered fix not completed} | 6.4 |`
- **Abstract, last sentence:** unchanged (18 words): "A registered count-matched leaderboard failed its fidelity check and was not scored, so no count-control result is confirmatory."
- **§8.4 and sec11:** unchanged. The PD-15 sentence stays.

## 9. Files

- **New:**
  - this file;
  - `scripts/lvlm/n9_rescue.py`: cap, start rule, gates, the attempt-2 scoring wrapper, `--selftest`;
  - `scripts/lvlm/n9_rescue_job.sh`: M3 stages (stage, base, methods, cleanup), `--selftest`;
  - `scripts/lvlm/SHA256SUMS`.
- **Unchanged and sha-pinned in that SUMS:**
  - the parent pair;
  - the K2 addendum;
  - `decode_llava.py`, `e1_chair_count.py`, `score_k2_n9.py`;
  - `data/coco_probe/chair500_ids.txt`, `data/coco_probe/chair500_val2014.sha256`;
  - `data/results/n9_k2/e1check.json`.
- `scripts/queue/jobs/m2_05_e1_k2_placebo.sh` and `m2_06_n9_leaderboard.sh` stay as the record of the 10-18 M2 runs. They are not used again.

## 10. Amendments

(none yet)

### Amendment 1 (2026-10-28): decode venv `/root/venv-n9` (OPS-1028m-op)

**Why.**
- `base 1` stopped on M3 before any GPU second was charged (0 GPU-s in the ledger). The stop came from `decode_llava.py`'s own dependency check (`main()`: sentencepiece and google.protobuf, which the slow Llama tokenizer needs): "missing dependency google.protobuf".
- M3's `/root/vsps/.venv`, at the `setup_gpu.sh` H_VS freeze, has sentencepiece but no protobuf. Neither does any other M3 venv.
- The 10-18 M2 venv that decoded the K2 pair and the failed batch-8 base had `protobuf==7.36.2` (`.session_backup/machines/O-2308428/root/outputs/claude_ops/m2_venv_pre_sklearn.txt` l.57). It also had the same transformers 4.51.3, torch 2.5.1+cu121 and sentencepiece 0.2.2 as H_VS.
- protobuf 7.36.2 is on PyPI, uploaded 2026-09-17, with a cp310 abi3 manylinux x86_64 wheel.
- Stage had already passed (OPS-1028l-op), and the N9 lock is still held.

**Venv design.**
- A dedicated `/root/venv-n9`, built from `scripts/lvlm/venv_n9_freeze.txt` (sha256 `193d4cc337451c548dc6c4f2ba9079c97e5682896115b43f8c0eaa1d7875fb4e`).
- That file is the H_VS freeze (`7332d343…`, 85 lines) plus exactly one line, `protobuf==7.36.2`, placed in pip's freeze order.
- `n9_rescue_job.sh` builds it once, if absent, the way `setup_gpu.sh` `mkvenv` builds `.venv`: python3.10 venv, `pip install --no-deps` from PyPI plus the cu121 torch index, py_vncorenlp as a PEP 517 build. CPU and online, so it is not charged to the cap.
- Before every decode stage (`base`, `methods`), the job checks that `pip freeze | sha256sum` equals that file's sha (`H_N9` in the job, and the file is pinned in `scripts/lvlm/SHA256SUMS`) and that `pip check` is clean.
- `decode_llava.py` (unchanged) then runs with `/root/venv-n9/bin/python`.
- A half-built venv fails the freeze check and stops the job. The operator removes `/root/venv-n9` before a retry.
- `/root/vsps/.venv` is not modified. K_F, scoring, every threshold, the cap, the start rule and the dates are unchanged.

**Check.** `n9_rescue.py --selftest` now asserts three things:
- the freeze file minus the protobuf line hashes to H_VS;
- the file is in pip order;
- it provides every module of `decode_llava.py`'s dependency check and every third-party import of its `main()`, parsed from the script: pillow, protobuf, sentencepiece, torch, transformers. H_VS alone fails this check.

**§6 gains deviation 8.** The decode stack on M3 is `/root/venv-n9`. It differs from the H_VS `.venv` by one package, `protobuf==7.36.2`, which the 10-18 M2 venv also had. This supersedes the software clause of §6 item 4. Each output still records its own stack.
