# C-ATTR-DEV block 1: run document

Version v1, written 2026-11-11T09:03Z (16:03 VN). Not committed. Nothing in block 1 has run. Label on every output file and row: `DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY`. AI opinion, not expert-validated.

Rule: `C_ATTR_DEV_PREREG_v1_1.md` (sha256 `44f81329d418efef823d466a4dca5fc9943817322cb3eef0afec7318c9d7681a`, commit 6d77729), §6.3, §9, §10; rulings CC-331 (gate 3: blocks 0–1 code and this document; N12) and CC-332 (notes 1–4). Where this document and the registration differ, the registration binds.

Wording, binding in every file, log line, row label and report: `lmcap_rand` / `lmcap_perm` = "a re-implementation of the LMCap recipe by this study"; `ret_img` vs `rand_img` = "an image–caption-pair prompt format, as used by RAGCap; not RAGCap"; no sentence says that a published system was tested. Every τ_pair / τ_marg row on OV-dev-A or OV-dev-B carries "split of a known τ_sel". Any planning-power figure carries "values are for m = 1". (Block 1 decodes none of the third-party arms.)

## 0. Host-side block 0 and checks (before any block-1 decode)

By the PI's instruction of 2026-11-11 (16:0x VN), no test runs on the laptop any more: self-tests, mutants, K0 list parity, refill diagnostics and the dry run all run on the rented host H1. **This replaces the laptop dry run of PI-1109g.** The five steps run in this order, after the host set-up of §3 (code, venvs, stored inputs restored; models may still be downloading) and before `c_attr_job.sh block1`. Each writes a log and its sha256 under `/root/outputs/c_attr_checks/`; **each is a STOP gate**: a non-zero rc, a SURVIVED mutant, a list-file sidecar check that is not OK, or a dry-run JOB STOP ends the session before any block-1 decode (fix on the laptop, new code read, re-push). All from `/root/vsps`, `C=/root/outputs/c_attr_checks; mkdir -p $C`:

| # | check | command | gate |
|---|---|---|---|
| 0.1 | self-tests | `for f in c_attr c_attr_lists c_attr_score; do /root/vsps/.venv/bin/python -I -B scripts/c_attr/$f.py --selftest; done > $C/selftest.log 2>&1; sha256sum $C/selftest.log > $C/selftest.log.sha256` (and `/root/venv-lb/bin/python -I -B scripts/c_attr/c_attr.py --selftest >> $C/selftest.log`) | rc 0, three "selftest ok" lines (+ venv-lb) |
| 0.2 | mutants | `/root/vsps/.venv/bin/python -I -B scripts/c_attr/c_attr_mutants.py --jobs 4 > $C/mutants.log 2>&1; sha256sum $C/mutants.log > $C/mutants.log.sha256` | "22/22 killed; survived: none", rc 0 (the control run must pass first; it needs numpy and scipy in the CPU venv) |
| 0.3 | K0 list parity | not re-run on the host: block 0 is registered on the laptop (§6.2) and passed there before PI-1111j (`scripts/c_attr/block0/K0_REPORT.json` `15108f2b…`: 911/911, 925/925, 500/500, fix f0 equal); `c_attr_lists.py build` refuses on a GPU host by design. Host check: `(cd scripts/c_attr && sha256sum -c c_attr_lists.json.sha256) > $C/k0.log 2>&1; sha256sum $C/k0.log > $C/k0.sha256` | "OK" and the sidecar names `8a2b977f…` (the committed list file); otherwise STOP, no list is "fixed" |
| 0.4 | refill diagnostics | read from the committed `scripts/c_attr/block0/K0_REPORT.json` `diagnostics` (counts and shares only): refill share at 8 slots per set and p (laptop record: max 0.000137) | > 0.10 on a set: `perm` is a diagnostic there (K0b); on OV-dev-B there is then no registered claim. Not a STOP for the other sets |
| 0.5 | dry run of every job mode | `C_ATTR_DRY=1 bash scripts/c_attr/c_attr_job.sh selftest <HEAD> && C_ATTR_DRY=1 bash scripts/c_attr/c_attr_job.sh block1 <HEAD>` (outputs under `/root/outputs/c_attr_dry`, never `c_attr`); then `cat /root/outputs/c_attr_dry/logs/*.log > $C/dryrun_logs.txt; sha256sum $C/dryrun_logs.txt > $C/dryrun.sha256` (job.log and every per-step log) | in `$C/dryrun_logs.txt`: `grep -c 'SELFTEST MODE DONE'` = 1, `grep -c 'JOB DONE'` = 1, `grep -c 'JOB STOP'` = 0, `grep -c '^DRY at_'` = 62, `grep -c 'prompt parity with .*: 2/2 equal'` = 5; otherwise STOP |

The checks run in the job's env (`HF_HUB_OFFLINE=1`, `NCS_DATA=/root/ncs-data`, machine id `h1`). Their GPU-h are not charged to the block-1 cap (CPU only). `$C/` is pulled with block 1 (§8).

## 1. Pinned inputs

| item | sha256 |
|---|---|
| `scripts/c_attr/SHA256SUMS` (c_attr.py, c_attr_lists.py, c_attr_score.py, c_attr_job.sh, c_attr_mutants.py, dryrun.sh, STORED_SHA256) | `d4e6363924711552aa1de5cb1e72ded4836e2bdc82e94c94ef5706a7a92b18ea` |
| `scripts/c_attr/C_ATTR_VS_C_T2.diff` (`diff -u` against `c_t2.py` 6113844a, for the code read) | `a118cc4e5e35aa48e916933cdad6717ebc703f51f79c98b936c317a5979be271` |
| `scripts/c_attr/c_attr_lists.json` (ids only; sidecar `.sha256`) | `8a2b977f9caf37f40bcc2a1b43e5b0c362b99d875ef28bc9640cccf2f9487cd5` |
| K0 / refill report `scripts/c_attr/block0/K0_REPORT.json` | `15108f2b1260770e4aa92fb44ae6301df45106b52a334d4b33068a4cf1028019` |
| laptop dry-run log `scripts/c_attr/block0/DRYRUN_LOG.txt` | `13bbb44d603f722fcbcff3f98b8c4d1956e3cdba317d9f913b3943d35f25432a` |
| mutant log `scripts/c_attr/block0/MUTANTS_LOG.txt` (22/22 killed) | `a7eef59372d5f25dac1d285fdbefccf0c6fa4b73f4dd66b61f432f5072726bbf` |
| stored runs and vectors: `scripts/c_attr/STORED_SHA256` (43 lines, from the sidecars of the M1/M3 backups) | in `SHA256SUMS` |

Already run on the laptop before the PI's instruction (2026-11-11, 07:59–09:02Z), kept as a record; §0 repeats each on the host as the binding run. Laptop results: K0 PASS — ret and rand d0 equal the stored lists on OV-dev-A 911/911, OV-dev-B 925/925, XM-dev500 500/500; the stored fix f0 equals on all three; Flickr30K val (not a K0 set) ret and rand d0–d2 1,014/1,014. Refill share at 8 slots ≤ 0.000137 on every set and p (gate 0.10): K0b passes everywhere. Images with π_1(q) = π_2(q): OV-dev-A 4, OV-dev-B 2, XM-dev500 0, Flickr30K val 0.

## 2. Preconditions (all before the rental)

1. Gate-3 code read GO on the package of §1 (CC-331 NEXT STEPS 5).
2. Commit through the gatekeeper: `scripts/c_attr/*` (code, `STORED_SHA256`, `SHA256SUMS`, `c_attr_lists.json` + sidecar, `C_ATTR_VS_C_T2.diff`, `block0/*`) and this document. `git diff --cached --name-only` holds only those paths; nothing with a caption is staged (`block0/` holds counts, shares and ids only).
3. The host-side checks of §0 all pass (they replace the laptop dry run of PI-1109g, PI instruction of 2026-11-11). The laptop dry run of §1 used a throwaway commit and an earlier `c_attr_job.sh` (before the `c_attr_dry` output split of the dry mode); it is a record only.
4. Money: L-before of the rented-GPU skill (cap 12 GPU-h × rate + 3 × rate + the other live rentals); PI-1110r: cost is not a decision factor, the check only prevents a stop for lack of balance.
5. Manual licence gates (CC-332 note / Q14, PI-1110i). The PI accepted the Gemma-3-4B licence gate himself (PI-1111h, LOG 2026-11-11T08:59:52Z); no PI line is needed for Gemma. Block 1 uses no gated-manual model.

## 3. Host

- One rented RTX 3090 or 3090 Ti 24 GB per the `running-rented-gpu-jobs` skill (spec, offer, facts, prep). Host H1 of §6.7. `/root/.vsps_machine_id` = `h1` (the job refuses any other id; the open() hook installs on `h1`/`h2`).
- Code: a sparse code-only clone at the committed HEAD: `scripts/`, `manuscript/prereg/`, `rescap/`, `configs/`, and the single tracked file `data/coco_probe/chair_synonyms.txt` (the C modules import `rescap.chair`, which reads it; found by the dry run). No other `data/` path. Check HEAD, `git diff --quiet`, every SUMS.
- Venvs: `/root/venv-lb` (freeze `685ffe2a…`, as C-T1/C-T2) and `/root/vsps/.venv` (CPU commands).
- Models (offline, `HF_HUB_OFFLINE=1`): `qwen25vl_7b`, `internvl3_8b` under `$NCS_DATA/models/<key>` by their B-N1 pins (setup_gpu.sh); Aya-Vision by `python scripts/c_attr/c_attr.py fetch --model aya_vision_8b --snapshot $NCS_DATA/models/c_t1_aya_vision_8b` (c_t1 registry pins, writes `.c_t1_ok`).
- Staged under `$NCS_DATA/datasets/` (nothing else there; the guard's allow-list): `ktvic/train_data.json` and `openviic/uit-openviic-annotation-train.json` (memory captions); `openviic/images/` = the 1,836 OV-dev-A + OV-dev-B files of `lists.json`, and nothing else; `c_xm_dev500/images/` = the 500 XM-dev500 files (the job checks the folder by sha). Pushed with the skill's six-stream transport and arrival check (manifest sha, `sha256sum -c` silent, counts, no links). No test image, no archive.
- Stored runs for step 1.0, restored to their host paths and checked by `grep -E 'ov_dev_[ab]-ret-' scripts/c_attr/STORED_SHA256 | sha256sum -c`: `/root/outputs/c_stage2/runs/c2_{qwen25vl_7b…k8-first-T1, internvl3_8b…k4-last-T2}` (OV-dev-B), `/root/outputs/c_t1/out/t1_aya_vision_8b_ov_dev_b-ret-k4-last-T1-mvi.preds.json`, `/root/outputs/c_stage1/runs/c1_{qwen25vl_7b…k8-first-T1, internvl3_8b…k4-last-T2}` (OV-dev-A, CC-331 N12).

## 4. Commands (inside tmux on H1, from `/root/vsps`)

```
bash scripts/c_attr/c_attr_job.sh selftest <HEAD>     # preflight only: SUMS, list sidecar, stored runs, venv freeze, selftests, guard, pins
bash scripts/c_attr/c_attr_job.sh block1   <HEAD>     # block 1, steps 1.0-1.5
```
Laptop helpers (watch, pull) run under `setsid nohup`, each with its own pid file. The job writes `/root/outputs/c_attr/{RUNNING, HEARTBEAT, gpu_seconds.tsv, logs/, out/, parity/, SHA256SUMS}`.

## 5. Steps, caps, timeouts, drop order

| step | content | captions (registered) |
|---|---|---|
| 1.0 | per backbone: check (a) host parity, first 50 OV-dev-B `ret` items in the stored order and batch slices (Qwen2.5-VL decodes 52 so that its batch-4 slices equal the stored ones; 50 are compared); **CC-331 N12:** check (a) also on the first 50 OV-dev-A `ret` items of Qwen2.5-VL and InternVL3; check (b) A1, the same 50 OV-dev-B items reversed at batch size 1 against this host's (a) decode | **300 registered + 100 per CC-331 N12** (about 0.26 + 0.03 GPU-h) |
| 1.1 | Qwen2.5-VL `perm` p1, p2 on OV-dev-A, OV-dev-B, XM-dev500 | 4,672 |
| 1.2 | Aya-Vision `zs`, `ret`, `rand` d0 on XM-dev500; `perm` p1, p2 on OV-dev-B, XM-dev500 | 4,350 |
| 1.3 | InternVL3 (τ = −∞, no deletion step) `perm` p1, p2 on the three sets | 4,672 |
| 1.4 | Qwen2.5-VL `fix` f1–f4, OV-dev-B first, then XM-dev500 | 5,700 |
| 1.5 | `rand` d1, d2 on XM-dev500, all three | 3,000 |

- Cap 12 GPU-h for the block (b1.left on `gpu_seconds.tsv`). Each GPU step runs under `timeout` for the time left; rc 124 is a CAP STOP, final; every later step is NOT RUN. Steps run in the order above, so the cap drops them from the bottom: 1.5, the XM-dev500 half of 1.4, 1.4, 1.3 (§6.3).
- A failed step resumes from its own partial file, at most 3 attempts, then JOB STOP (§10.2). Any refused image or set stops the step before the model load.
- Host-parity fallback (§6.3, K1b): a backbone with any check (a) failure (OV-dev-B or, per CC-331 N12, OV-dev-A) gets `zs`, `ret`, `rand` d0 decoded again on H1 before its `perm` step, for the sets of its `perm` step (Qwen2.5-VL and InternVL3: OV-dev-A, OV-dev-B, XM-dev500; Aya-Vision: OV-dev-B). Its rows then use the new-host arms only (R = 1), carry "base arms re-decoded on the new host", and stay in their families. Strict reading taken: one parity verdict per backbone covers all its perm sets.
- A1 failure (K1): recorded in `parity/STEP10_<model>.json`; that backbone's rows are printed as "A1 not met" and leave the families; nothing is dropped.
- Point projection 7.4 GPU-h (high 11.1) + 0.03 (N12); with all three fallbacks +5.5 at point rates, so a binding cap is possible only with fallbacks: the drop order above then applies.

## 6. Monitoring (§10.4)

Only `logs/job.log` lines (START / OK / FAIL / CAP STOP / JOB STOP / STEP 1.0 verdict lines), the age of `HEARTBEAT`, `gpu_seconds.tsv`, return codes. No caption, no per-image score, no partial ledger. The step-1.0 comparators print counts and item ids only.

## 7. Kill gates in block 1

| id | where | consequence |
|---|---|---|
| K0 | block 0 | PASSED (§1) |
| K0b | block 0 | passed on every set (refill share ≤ 0.000137) |
| K1 | step 1.0 (b) | the backbone leaves the families |
| K1b | step 1.0 (a) | fallback of §5; nothing dropped |
| K2 / K3 | after the nomination / the OV-dev-B look (§8 below) | as the registration |
| K7 | 2026-11-16 12:00 VN | every unfinished step NOT RUN |

## 8. Pull, verify, 444, scoring order, nomination hash

1. Only after `JOB DONE` or `CAP STOP` in `job.log` and `RUNNING` gone: pull `/root/outputs/c_attr/` to `.session_backup/machines/ATTR_H1/root/outputs/c_attr/`; `sha256sum -c SHA256SUMS` there (all OK; counts equal); `chmod -R a-w` (files 444). Scoring reads the 444 copy only. Then wipe and delete the host (logged), L-after.
2. Scoring parity gate (§7.1): the first `c_attr_score.py score` call on OV-dev-B passes `--c2-dir` and `--c2-ledger` (stage-2 parity within 1e-4); a mismatch stops scoring.
3. OV-dev-A first: `c_attr_score.py score --set ov_dev_a --runs <stored zs, ret, rand d0 of Qwen2.5-VL and InternVL3 (or their new-host arms)> <new perm p1, p2> --ledger L_A …`.
4. **Nomination hash step (§7.5 item 2):** `c_attr_score.py nominate --ledger L_A --out c_attr_nomination.json`; the command refuses if any OV-dev-B `perm` score exists. The coordinator writes its sha256 to the decisions LOG **before** any new OV-dev-B output is scored or opened.
5. OV-dev-B: `c_attr_score.py score --set ov_dev_b … --nomination c_attr_nomination.json` (refused without it when a `perm` run is given); then XM-dev500; then `c_attr_score.py summary --ledger … --nomination c_attr_nomination.json --out c_attr_summary.json` (DETECTED by Holm step-down at family-wise one-sided 0.025, §7.4).
6. Not here: the copy bound (step 0.3) and the other block-0 CPU rows wait for the code read GO; they are not part of block 1.

## 9. Block-1 report (to the coordinator; Vietnam time from `date`)

One block: "Step 1.0: 300 registered + 100 per CC-331 N12 captions; host parity (a) per backbone PASS/FAIL; A1 (b) per backbone PASS/FAIL; fallbacks run; steps OK / NOT RUN; GPU-h used of 12; pull verified (n files, SHA256SUMS OK); host deleted."

## 10. Not in this document

Blocks 2–4 (new backbones, third-party arms, English); their job modes are not written. `c_attr_registry.json` (block-2 pins) is not written.
