# L1-b AMENDMENT 2: host loss during run 2 (rr_idefics3_8b), relaunch on a new M2

Amends PREREG.md (sha b6034c4a, unchanged) and AMENDMENT_1.md (sha 037d2ec0, unchanged). Written 2026-10-30, before
`score` has run. Tier 1 (DEV-EXPLORE, ViTextVQA dev half E only). AI opinion, not expert-validated. Judge: CC-177
(single judge, reversible tier ≥ 90): GO-with-fixes 91%, Q1 (a), Q2 R; W1–W3 applied in this text. Code, registry, split, prompt, batch sizes, parity rule and tolerance, the
selection grid and every decision rule are unchanged. This is not a parity amendment (AMENDMENT_1 §8).

## 1. What happened

| UTC (2026-10-29) | Event |
|---|---|
| 18:56:30 | Run 2 JOB START at 285fcbf7 (AMENDMENT_1 §8), gemma skipped, idefics3 decode skipped (sidecar) |
| 18:56:31 | START rr_idefics3_8b; `gpu_seconds.tsv` gets `rr_idefics3_8b start 1793300191` |
| 20:41:20 | last full backup pull of M2 /root (laptop mirror) |
| 20:53:12 | last successful ssh contact with M2 (backup "CRIT") |
| 21:01:55 | first unreachable contact (rc 255) |
| ~21:30 | rental expiry reported by the PI (OPS-1030i); all on-host data lost |
| 21:45:00 | coordinator records M1 and M2 gone (OPS-1030h) |

No `score` has run (`.session_backup/2026-10-29/l1b/decide.json` does not exist). Only rr_idefics3_8b was running;
qwen25vl_7b, internvl3_8b and qwen3vl_8b reranks of run 2 never started.

## 2. What survives (laptop mirror, by sha only; no content opened)

Snapshot copy `.session_backup/2026-10-30/l1b_amend2/mirror_snapshot_M2_l1b/` + sha list d2a3a40a (23 files).
- `out/l1b_idefics3_8b_img.preds.json` ec3f8478 = its sidecar = AMENDMENT_1 §5 / `REUSE_DEC` pin.
- `out/l1b_idefics3_8b_rerank.jsonl` af1fb6ea, 1,740 lines (header + up to 1,739 fsynced items of 2,210; the
  last line may be torn by the copy). Written by l1b.py 391f1e88 at 285fcbf7 (run key below).
- `gpu_seconds.tsv`: 4,587 s closed (1.27 h, AMENDMENT_1 §7) + the open `rr_idefics3_8b start 1793300191`.
- The mirror is a no-`--delete` superset: `out/` still holds two AMENDMENT_1 §6 files that were moved on the host
  (`l1b_idefics3_8b_PARITY_FAIL.json` 1acd933e, old-key `l1b_qwen25vl_7b_rerank.jsonl` 3697e9e5), plus a stale
  `RUNNING`. Restored as is, they would make idefics3 NOT_ASSESSABLE without running, stop qwen25 on "run key
  differs", and block the lock.

## 3. Rulings asked of CC-177

**Q1. The open start line.** `b1.used_seconds` charges an open start to the next start line or to now. Left as is,
the first `left` call at relaunch charges 18:56:31Z → relaunch (≥ 9 h with the downtime) and the job CAP STOPs,
final, before any GPU step. Before the relaunch one line `rr_idefics3_8b <SECONDS>` is appended, closing the step:

| Option | End point | Charged | Total | Left of 8 h |
|---|---|---|---|---|
| a (recommended) | 21:45:00Z, host recorded gone (upper bound with evidence) | 10,109 s | 4.08 h | 3.92 h |
| b | 21:30:00Z, reported expiry (approximate) | 9,209 s | 3.83 h | 4.17 h |
| c | 21:01:55Z, first unreachable (the GPU may have run on) | 7,524 s | 3.36 h | 4.64 h |
| d | none (code default, charge to relaunch) | ≥ 8 h | cap | 0: CAP STOP |

(a) cannot undercount: the job cannot have run after the host was gone. (b)/(c) may undercount. **Ruled (CC-177):
(a).** The exact closing line is `rr_idefics3_8b 10109`. The code default (d) is overruled on the record: the downtime
was not GPU time.

**Q2. The partial rerank: resume or restart.**
- **R (recommended): resume.** PREREG §5.5: "an interrupted rerank resumes from its fsynced items under the same run
  key only". The run key is sha256 of [l1b.py sha, split sha, base-preds sha, model revision, cand batch]; all are
  unchanged (l1b.py 391f1e88, split b749f720, base ec3f8478, pinned idefics3 revision, registry batch). It does not
  include git HEAD, so this amendment's commit does not change it. `cmd_rerank` drops a torn last line, refuses a
  different key, and re-scores the first PARITY_N = 4 items on the new host for the parity gate before skipping done
  items, so the parity check runs again on the new host.
  **Disclosure (CC-177 W3):** items are scored on two hosts. Same: GPU model RTX 3090 24 GB, venv-lb freeze 685ffe2a
  (enforced by the job preflight), snapshot revision, code and run key. Different: host 2 has 16 CPU and 31 GB RAM
  (host 1: 62 GB; OPS-1030k-op) and driver 595.99.02 (host 1's driver is in its rebuild record). The rerank header
  records host 1's git_head, GPU and machine only; `l1b_idefics3_8b_parity.json` will hold host 2's items 0–3 only.
  bf16 kernels are non-deterministic even on one host (AMENDMENT_1 §2B), so mixing adds no new kind of noise. The
  judge checked one byte of the partial file, its last byte (a newline): no torn last line, 1,739 items done,
  471 remain. No other content was read.
  Cost: about 471 items × 3.6 s (observed run-2 rate) + load ≈ 0.55 h.
- **D: restart.** Move the partial to `superseded_285fcbf7/` unread; idefics3 rerank from item 0, ≈ 2.4 h.

Remaining work (CC-177 W2; the measured run-2 idefics3 rate is 1.09× its AMENDMENT_1 estimate, and the Qwen-family
estimates are scaled the same way; loads ≈ 0.3 h): R ≈ **4.0 h** against 3.92 h left, so qwen3vl_8b (last) will
probably be CAP-STOPped and NOT_ASSESSABLE, leaving 3 backbones in use, and §6 still gives a verdict. D ≈ 5.8 h:
only idefics3 and qwen25 would finish, close to a certain NO_VERDICT. A timeout stays a final CAP STOP (CC-168 W4a).
The cap stays 8 GPU-h (CC-173). **Ruled (CC-177): R.**

The earlier "partials are deleted before a retry" practice concerned retries after a code or key change. Here code
and key are unchanged and the prereg names resume as the rule.

## 4. Relaunch (same run, same output dir, new host)

1. New M2 built by `setup_gpu.sh` (ROLE m4, OUT_MIRROR M4; host check pins updated to the new hosts, OPS-1030k-op).
2. Upload to M2 `/root/outputs/l1b` exactly the 20 files of `.session_backup/2026-10-30/l1b_amend2/upload_manifest.sha256`
   (cb4c933c): the snapshot minus `out/l1b_idefics3_8b_PARITY_FAIL.json`, `out/l1b_qwen25vl_7b_rerank.jsonl` and
   `RUNNING` (all three already kept under `superseded_58160ccf/` or stale). `sha256sum -c` on M2. Under option D,
   also move `out/l1b_idefics3_8b_rerank.jsonl` to `superseded_285fcbf7/`.
3. Append the Q1 closing line to `gpu_seconds.tsv`.
4. Stage dev-E as OPS-1029u-op (743 files: 738 E jpgs, grey.png c6bf3833, questions.jsonl d3a8cfae without answers,
   3 L1-a img preds ebfddfa7/c4cf7cab/9cc4db18). No gold, no train or test file.
5. Move M2 to the HEAD that commits this file (git bundle, ff-only, clean tree, l1a/l1b/prereg SUMS OK); run the
   selftest; `bash scripts/l1b/l1b_job.sh <HEAD>` in tmux `l1b`. The job fetches idefics3_8b itself (CPU, not
   charged). Order unchanged: idefics3_8b (resume) → qwen25vl_7b → internvl3_8b → qwen3vl_8b.
6. **Stale mirror (CC-177 W1).** Before the backup loop starts on the new M2, the old mirror directory
   `.session_backup/machines/M2/` is renamed to a quarantine name (`M2_host1_lost_1029`); the 23-file snapshot copy
   (§2) already exists, so nothing is lost. The backup then fills a fresh `M2/`. `score` (laptop, once, not by the
   operator) reads only a folder whose `out/` and `logs/` match the new host's SHA256SUMS exactly.
7. Operator checks before tmux `l1b` (CC-177 W4/W5): `/root/rebuild_tmp/dl.log` ALL DONE with no FAIL; the three
   `l1b.py snap --model` directories (qwen25vl_7b, internvl3_8b, qwen3vl_8b) exist; staged preds/ shas equal
   L1A_IMG_SHA; after the append, `l1b.py left` ≈ 14,104 s, and the post-append sha of `gpu_seconds.tsv` is logged.

## 5. No outcome seen

No rerank or preds content was opened by a person or agent; files were handled by sha, size and line count only.
No gold is on any machine.

## 6. Pins

This file is added to the prereg SHA256SUMS (5 entries). l1b.py, l1b_job.sh, scripts/l1b/SHA256SUMS, PREREG.md,
registry, split and AMENDMENT_1.md are unchanged.
