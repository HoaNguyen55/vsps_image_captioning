# C-ATTR-DEV block 3 (the positive control): run document

Version v1.1 = v1 (sha256 `ec0928ae…`) + the fixes R0–R4 of ruling CC-368, applied by script. v1 written 2026-11-12 (UTC 15:50–17:00, `date -u`). Nothing in block 3 has run; no block-3 output exists. Label on every output file and row: `DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY`. AI opinion, not expert-validated.

Rule: registration `C_ATTR_DEV_PREREG_v1_1.md` (`44f81329…`) §2, §4, §6.5, §6.7, §7.4, §7.10, §9, §10; erratum 1 (`f9f0842e…`, E6 labels); addendum v1.2 (`5858d69d…`) V8 (batch size 1, D1 per backbone, cap min(12, 1.5 P3)) with the V7 formula; rulings CC-341, CC-346, CC-348, CC-362, CC-363 (ruling 6: block 3 first; a run document, a code diff, a one-judge read as a new topic, then a decode on a host with no other job). Where this document and the registration differ, the registration binds, except for the departures ruled by CC-368 before any block-3 output existed: (i) the re-decodes of `lmcap_ri` and `ret_img` on OV-dev-B (§2 steps 1 and 7; §12 O1) are a disclosed deviation from the decode list of v1.1 §6.5 and from v1.1 §6.3 "every stored run is reused"; for block 3 they bind, no stored decode enters a block-3 contrast, and every block-3 row carries "all arms decoded on one host in block 3; stored decodes not used (CC-368)"; (ii) D1 is made per runner on the arm that runner decodes in block 3 (LMCap `lmcap_ri`, Qwen2.5-VL `ret_img`), in place of the `ret` items of V3 (§12 O2, O3); (iii) P3 and the cap min(12, 1.5 P3) of V8 are computed over all ten steps of §2, the re-decodes included, at the D1 rates, and the 12 GPU-h ceiling is unchanged (§12 O5). Every other under-specified point this document reads is listed in §12; the reading that binds is the one ruled in CC-368.

Wording, binding in every file, LOG line, row label and report (erratum E6): LMCap rows carry "re-implementation of the LMCap recipe by this study; not the authors' code (no licence); not a statement about the published numbers"; the `ret_img` against `rand_img` row carries "image-caption-pair prompt format, as used by RAGCap; not RAGCap" (the row name "RAGCap-style" is withdrawn). No sentence says that a published system was tested. Nothing on this page names a host address.

Code: `scripts/c_attr/` at the commit that holds `C_ATTR_B3.diff` (diff against HEAD `d10874e`, whose `scripts/c_attr/` equals eb4286a) and the new `scripts/c_attr/SHA256SUMS` (§1).

## 0. What block 3 is

Registered text (v1.1 §6.5, quoted):

> ### 6.5 Block 3: third-party re-implementations, Vietnamese (hard cap 5 GPU-h)
> | 3.1 | `lmcap_rand`, `lmcap_perm` | OV-dev-B (925) | 1,850 | 0.59 |
> | 3.2 | `lmcap_ri`, `lmcap_rand`, `lmcap_perm` | XM-dev500 (500) | 1,500 | 0.48 |
> | 3.3 | Qwen2.5-VL `rand_img` d0 (k = 8) | OV-dev-B (925) | 925 | 0.90 |
> | 3.4 | Qwen2.5-VL `ret_img`, `rand_img` d0 | XM-dev500 (500) | 1,000 | 0.98 |
> | **block 3** | | | **5,275** | **2.9** (high 4.4) |
> Steps 3.3 and 3.4 need the images of the 8,190 cluster representatives on the host, checked by sha256 before any GPU step (the `memcheck` of C-T1 PREREG l.74).

Addendum V8 (quoted): "Blocks 3 and 4: every decode that enters a contrast row is at batch size 1 (ret_img/rand_img are already batch 1), with D1 per backbone. Caps: block 3 = min(12, 1.5 P3), … with P from the V7 formula at measured r_b; drop orders unchanged."

Purpose (v1.1 §7.10, quoted): "**Positive control:** LMCap's generator never sees the image; image information enters through retrieval and through the M-CLIP re-rank of the three beams. τ_sel must be DETECTED on OV-dev-B. If it is not, the test failed a case with a known answer (§10.1, K5)." Kill gate K5 (11-15): "LMCap τ_sel not DETECTED on OV-dev-B → the positive control failed; the word 'test' is dropped; third-party rows are printed without interpretation." CC-363 (ruling 5, "Does not support"): "The word 'test' for the method (the positive control was not run)." Block 3 is the only block that can answer K5.

Estimands (v1.1 §7.10): LMCap τ_sel = `lmcap_ri` − `lmcap_rand`; τ_pair = `lmcap_ri` − `lmcap_perm`; τ_marg = `lmcap_perm` − `lmcap_rand` (`lmcap_perm` uses p = 1 only, §2); image-caption-pair format τ_sel = `ret_img` − `rand_img` for Qwen2.5-VL, beside its text-only τ_sel. Labels of §7.4 (m = 1: no family).

Hosts (v1.1 §6.7): "No job runs beside another on one host." The job refuses while a GPU compute process exists or another C-ATTR `RUNNING` file is present (§5).

## 1. Code and pinned inputs

| item | sha256 |
|---|---|
| `scripts/c_attr/SHA256SUMS` (8 files) | `ecd37cc724557ce25a5e9b401592e1a9b05edc2eef5276cee08102094c1bc9ce` |
| `scripts/c_attr/c_attr.py` | `a3bd7b93bdcc85cc6ce34a0676796cafd4e23497f3deae17b3f6ff60f2e31dc0` |
| `scripts/c_attr/c_attr_job.sh` | `d367f3c63e83e21c4f6731f8e472ffe3e5c95fdb0062932d471493725aa04f2a` |
| `scripts/c_attr/c_attr_mutants.py` | `12b0c0a6caea40ae5f70ad269fed4c8485e14502f0d2345f4ec85197d2f7802f` (A6 pattern anchored, CC-368 W1) |
| unchanged: `c_attr_lists.py` 494a0e56, `c_attr_score.py` bb2077b9, `c_attr_score_job.sh` 80b48f00, `dryrun.sh` 3dce71cc, `STORED_SHA256` b12030dc | as in SHA256SUMS |
| `scripts/c_attr/C_ATTR_B3.diff` (= `git diff HEAD -- scripts/c_attr`, 4 files, +241 / −25) | `621e81c7316d22ba8cc3e30bb9038fbe5428339bfe4e8bbdb8433b759727b168` |
| list file `scripts/c_attr/c_attr_lists.json` (ids only; `donor` lists for p = 1, 2 on OV-dev-B and XM-dev500) | `8a2b977f…` (sidecar) |

What the diff changes, and nothing else (decode side only; the scorer is untouched):
- `cmd_lmcap`: refuses an existing run id ("decoded once", as `decode`) and a `fwd50` without `--batch1`; `--redecode rev50|fwd50` (variant `ri` only) for D1; `--batch1` adds `-b1` to the id (LMCap decodes one image per `generate` call, so its batch size is always 1; the record now says `batch_size: 1`); `--dry-run` stops before the model load; load and decode seconds are recorded apart (`timing`, as `decode` since v1.2); the GPU imports moved after the dry-run return; the `lmcap_perm` list file is named after the run id. The decoding itself (shots, retrieval, prompt, beam 3, re-rank) is byte-unchanged.
- New: `lmcap_run_id`, `d1_items`, `b3_steps`, `plan3`, `cmd_plan3` (`plan3` subcommand), `B3_*` constants.
- Isolation hook: `/root/outputs/c_attr_b3` added to the writable output folders (else the hook denies the job's own writes).
- `c_attr_job.sh`: mode `block3` (§4); for that mode the preflight checks only what block 3 reads (Qwen2.5-VL snapshot, LMCap pins, venv-t1 freeze `1766dc23…`, `t1check`, `memcheck` of the 8,190 representatives, the three stored SigLIP2 vector files, addendum `SHA256SUMS_1B`, c_t1 registry `SHA256SUMS`). Modes `selftest`, `block1`, `block1b` are unchanged in behaviour.
- Self-test `selftest_b3` (step order and counts, cap min(12, 1.5 P3) from D1 timings, LMCap ids and D1 reference, the D1 slice, LMCap refusals before any model load, the `c_attr_b3` folder); mutants B1–B10 (one per new rule).

**No new backbone, so no new-backbone registry.** XGLM-2.9B (`facebook/xglm-2.9B` @ `33c659ae…`, 7 files), M-CLIP (`laion/CLIP-ViT-H-14-frozen-xlm-roberta-large-laion5B-s13B-b90k` @ `f9ab9552…`, 3 files) and `xlm-roberta-large` (@ `c23d21b0…`, 4 files) are fully pinned (no null hash) in the committed `manuscript/prereg/2026-10-30_c_t1/c_t1_registry.json` (`09e6f90a…`, its `SHA256SUMS`), and Qwen2.5-VL-7B by the B-N1 block (`cc594898…`). `c_attr_registry.json` (v1.1 §11.1) belongs to block 2 and is not written here; no pin was taken by hashing a fetched file.

## 2. Decode list, in order (every run at batch size 1, every id with `-b1`; outputs in `/root/outputs/c_attr_b3/out/`)

| # | step | runner | arm | set | captions | registered as |
|---|---|---|---|---|---|---|
| 3.0a | D1, LMCap | LMCap re-impl. (venv-t1) | `lmcap_ri` first 50 OV-dev-B items, reversed (`rev50`), then forward at batch 1 (`b1-fwd50`) | OV-dev-B | 100 | V8 D1 (reading §12 O2) |
| 3.0b | D1, Qwen2.5-VL | Qwen2.5-VL (venv-lb) | `ret_img` (k 8, first, T1) first 50 OV-dev-B items, `rev50` then `b1-fwd50` | OV-dev-B | 100 | V8 D1 (reading §12 O3) |
| 1 | B3_lmcap_ov_dev_b_ri | LMCap | `lmcap_ri` | OV-dev-B | 925 | re-decode on this host (§12 O1) |
| 2 | B3_lmcap_ov_dev_b_rand | LMCap | `lmcap_rand` | OV-dev-B | 925 | 3.1 |
| 3 | B3_lmcap_ov_dev_b_perm | LMCap | `lmcap_perm` (p = 1; its list file written and hashed before its decode, §9 A2) | OV-dev-B | 925 | 3.1 |
| 4–6 | B3_lmcap_xm_dev500_{ri,rand,perm} | LMCap | `lmcap_ri`, `lmcap_rand`, `lmcap_perm` | XM-dev500 | 1,500 | 3.2 |
| 7 | B3_qwen25vl_7b_ov_dev_b_ret_img | Qwen2.5-VL | `ret_img` | OV-dev-B | 925 | re-decode on this host (§12 O1) |
| 8 | B3_qwen25vl_7b_ov_dev_b_rand_img | Qwen2.5-VL | `rand_img` d0 | OV-dev-B | 925 | 3.3 |
| 9–10 | B3_qwen25vl_7b_xm_dev500_{ret_img,rand_img} | Qwen2.5-VL | `ret_img`, `rand_img` d0 | XM-dev500 | 1,000 | 3.4 |
| | **total** | | | | **7,125 + 200 D1 = 7,325** | registered 5,275 + 1,850 re-decodes + 200 D1 |

Backbones × sets × arms: LMCap 3 arms × 2 sets (6 runs, 4,275 captions); Qwen2.5-VL 2 arms × 2 sets (4 runs, 2,850 captions). Run ids: `at_lmcap-<variant>_<set>-mvi-b1`, `at_qwen25vl_7b_<set>-ret_img-k8-first-T1-mvi-b1`, `at_qwen25vl_7b_<set>-rand_img-k8--T1-d0-mvi-b1`.

**D1 (V8, V3 form).** For each runner, the forward batch-1 decode of the first 50 OV-dev-B items must equal, as strings, 50/50, this host's reversed batch-1 decode of the same items (`compare --d1`, counts and failing ids only; it refuses any other reference by run id and batch size). The verdict goes to `parity/STEP3_<runner>.json`. A FAIL removes that runner's block-3 steps (NOT RUN); for LMCap that means K5 is NOT RUN, reported as such, and no re-registration is made for the failure. The D1 files are never scored.

## 3. Cap and GPU-hour projection

- Formula (V7 via V8): P3 = Σ over the steps of the D1-passing runners of (N · r_b + L_b) / 3600, with r_b = decode seconds per caption and L_b = load seconds, both read from that runner's forward D1 file (`timing`). Hard cap = min(12, 1.5 · P3) GPU-h. `plan3` writes `CAP_3.json` and `STEPS_3.tsv`; the D1 seconds count against the cap (as in 1b); during D1 the 12 GPU-h ceiling applies.
- For LMCap, L_b covers the two model loads, the M-CLIP encoding of the 8,190 memory captions and the shots; the `lmcap_perm` list (925 donor image encodings) falls in the load part of its own run and is not in the D1 L_b (small; stated, not corrected).
- Planning values (registration §6.1 point rates from `gpu_seconds.tsv` of C-T1/C-T2, model load included: LMCap Vietnamese 1.14 s per caption; `ret_img` 3.52 s; XM-dev500 assumed equal to OV-dev-B, chưa kiểm): LMCap 4,275 × 1.14 = 4,873.5 s; Qwen2.5-VL 2,850 × 3.52 = 10,032 s; **P3 = 14,905.5 s = 4.14 GPU-h**, cap at planning rates **min(12, 6.21) = 6.21 GPU-h**. D1 adds 100 × 1.14 + 100 × 3.52 = 466 s (0.13 h): **projection 4.27 GPU-h**, high (× 1.5) 6.4 GPU-h. The registered list alone is 2.94 h (§6.5); the re-decodes of §12 O1 add 1.19 h.
- The binding cap is the one computed from the D1 rates; it is written to the LOG after D1 and before step 1 (PAUSE, §4). Because the cap scales with the measured D1 rates, it binds only if the steps run about 1.5× slower than their own D1 rate (for example a slower XM-dev500 set), or if P3 exceeds 8 h (the 12 GPU-h ceiling); steps then drop from the bottom of §2 (Qwen2.5-VL XM-dev500 first; LMCap OV-dev-B last).
- Wall time for the decodes about 4.3 h plus host set-up; K7 (2026-11-16 12:00 VN = 05:00Z) and K5 (dated 11-15) bound the start. Planning value: launch call 1 by 2026-11-15T00:00Z (07:00 VN); later than that leaves too little room for decode, pull, scoring and the read before K7.

## 4. Commands (tmux on the block-3 host, from `/root/vsps`; no other job on the host)

```
bash scripts/c_attr/c_attr_job.sh block3 <HEAD>   # call 1: preflight, 3.0a/3.0b D1, plan3, PAUSE
bash scripts/c_attr/c_attr_job.sh block3 <HEAD>   # call 2, after the LOG cap line: steps 1-10 under the cap
```

- Preflight STOPs on: HEAD or tracked files differ; GPU busy; any SUMS (code, registration, `SHA256SUMS_1B`, c_t1 registry); `/root/outputs/c_attr/RUNNING` or `/root/outputs/c_attr_b1/RUNNING`; the three stored vector files (`c_stage1/emb.npz` 59e65f6f, `c_stage2/emb_ov_dev_b.npz` 5ad23a67, `c_stage2/emb_xm_dev500.npz` 48ec2476, by `STORED_SHA256`); list sidecar; venv-lb freeze `685ffe2a…`; venv-t1 freeze `1766dc23a71509ba4fb6b8adb34b1999a3a2bf78ebe1e227730fd6647bea3599`; self-tests (venv-lb, venv-t1, `c_attr_lists`); the custody guard; Qwen2.5-VL snapshot dir; `pinsok` for XGLM and M-CLIP; `t1check` (M-CLIP built offline); `memcheck` of `memfiles_vi.json` (every one of the 8,190 representatives present with its sha256).
- **PAUSE.** Call 1 ends with `PAUSE after D1 …` and the sha256 of `CAP_3.json`. The coordinator then writes one LOG line before call 2: the two D1 verdicts and identical counts (`parity/D1_<runner>.json`), r_b and L_b of each runner, P3 and the cap, the `CAP_3.json` sha256. A D1 decode that needed more than one attempt (a `START D1_…` line with attempt 2 or 3) under-counts its decode seconds: STOP before call 2, back to the judge. Call 2 writes `STEP3_*.json` and `D1_*.json` again with a new time stamp, so their sha256 are logged from the final pull; a verdict there that differs from this line is a STOP before any score. `CAP_3.json` is never deleted or remade after that line without a judge line.
- Steps: each under `timeout` for the time left; rc 124 = CAP STOP, final, every later step NOT RUN. A failed step: at most 3 attempts, then JOB STOP. The Qwen2.5-VL decodes resume from their partial file; an LMCap run has no partial file, so a retry decodes the run again from its first item (§12 O7). Any refused image or set stops the step before the model load. K7: every unfinished step NOT RUN.
- A CAP STOP, JOB STOP or K7 before step 2 (`lmcap_rand` on OV-dev-B) is OK leaves K5 without its two arms: K5 is then reported NOT RUN; no block-3 row is scored until a judge line.

## 5. Host gates before any block-3 decode (each a STOP gate; CPU only; not charged to the cap)

All from `/root/vsps`, with `C=/root/outputs/c_attr_checks_b3; mkdir -p $C`, in the job's environment (`HF_HUB_OFFLINE=1`, `NCS_DATA=/root/ncs-data`, machine id `h1`). A non-zero rc, a SURVIVED mutant or a dry-run JOB STOP ends the session before any decode; the fix is made on the laptop and goes through a new read.

| # | check | command | gate |
|---|---|---|---|
| b3.g0 | inputs of record | `sha256sum` of `$NCS_DATA/datasets/c_t1_mem/memfiles_vi.json`, `ktvic/train_data.json`, `openviic/uit-openviic-annotation-train.json` > `$C/inputs.sha256` | begin `886af149`, `72ee9b57`, `d757520e` (the 8-hex values of record, OPS-1030g/n); one OPS line gives the full values; otherwise STOP |
| b3.g1 | self-tests (**OWED: never run on the changed code**) | `for f in c_attr c_attr_lists c_attr_score; do /root/vsps/.venv/bin/python -I -B scripts/c_attr/$f.py --selftest; done > $C/selftest.log 2>&1; for v in venv-lb venv-t1; do /root/$v/bin/python -I -B scripts/c_attr/c_attr.py --selftest >> $C/selftest.log 2>&1; done; sha256sum $C/selftest.log > $C/selftest.log.sha256` | rc 0; five "selftest ok" lines; the c_attr lines name "block 3: step order and counts (7,125) …" |
| b3.g2 | mutants (**OWED**) | `/root/vsps/.venv/bin/python -I -B scripts/c_attr/c_attr_mutants.py --no-netns --jobs 4 > $C/mutants.log 2>&1; sha256sum $C/mutants.log > $C/mutants.log.sha256` | control passes, then `83/83 killed; survived: none` (73 of record + B1–B10). Not network-isolated (`--no-netns`, CC-346 flag a) |
| b3.g3 | list sidecar | `(cd scripts/c_attr && sha256sum -c c_attr_lists.json.sha256) > $C/k0.log 2>&1` | "OK", `8a2b977f…` |
| b3.g4 | dry run of the new mode (**OWED: the block3 mode has never run, even dry**) | `C_ATTR_DRY=1 bash scripts/c_attr/c_attr_job.sh block3 <HEAD>` (outputs under `/root/outputs/c_attr_b3_dry`), then `cat /root/outputs/c_attr_b3_dry/logs/*.log > $C/dryrun_logs.txt; sha256sum $C/dryrun_logs.txt > $C/dryrun.sha256` | `grep -c 'JOB DONE'` = 1, `grep -c 'JOB STOP'` = 0, `grep -c '^DRY at_'` = 14 (4 D1 + 10 steps), `grep -c 'STEP 3.0 .* D1 PASS'` = 2, `grep -c '^PLAN 3: P3 4.14 GPU-h, cap 6.21 GPU-h, 10 runs, NOT RUN none$'` = 1 (the plan.log line; the self-test's own planted `PLAN 3:` lines in `selftest.log` read differently, and job.log repeats the line after a time stamp) |
| b3.g5 | tmpfs custody | `/root/vsps/.venv/bin/python scripts/c_attr/c_attr.py guard --roots /dev/shm/c_attr_b3 > $C/guard_tmpfs.log 2>&1` (the job's guard does not descend into symlinked image dirs) | "guard ok" |

Because the block3 mode is new, a defect found by b3.g1, b3.g2 or b3.g4 goes back to the judge with the fix; it is not patched on the host.

## 6. Monitoring (§10.4)

Only `logs/job.log` lines (START / OK / FAIL / CAP STOP / JOB STOP / STEP 3.0 / PLAN 3 / PAUSE), the age of `HEARTBEAT`, `gpu_seconds.tsv`, return codes. No caption, no per-image score, no partial file. The `lmcap_perm` list file is ids only; its sha256 is printed in the step log before the decode (A2) and goes into the report.

## 7. Pull, verify, 444

After `JOB DONE` or `CAP STOP` and `RUNNING` gone: pull `/root/outputs/c_attr_b3/` and `/root/outputs/c_attr_checks_b3/` to `.session_backup/machines/ATTR_H3/root/outputs/`; whole-tree digest equal to the host's; `sha256sum -c SHA256SUMS` in `c_attr_b3/` all OK except `logs/job.log` (appended after the sums, as OPS-1112c); `CAP_3.json` and `STEPS_3.tsv` lie outside `SHA256SUMS`: log their sha256 (`CAP_3.json` equal to the PAUSE line). Then `chmod -R a-w`. The host is kept only if the scoring package of §8 has a GO and runs there next; otherwise backed up and deleted (PI-1109g).

## 8. Scoring: what exists, what is missing (not licensed here)

This document runs no scoring command. What the committed scorer already covers:
- `c_attr.py score` (the V4 gates inside, SC1) scores LMCap runs with the stage-2 `plain_row` (stripped CIDEr-D, kit B, RDRSegmenter) plus a `masked3` row, and the `ret_img` / `rand_img` runs with the stage-1 `score_set` (it needs one Qwen2.5-VL `zs` per set: the pinned stage-2 runs `c2_qwen25vl_7b_ov_dev_b-zs` 5bf37a77 and `…_xm_dev500-zs` d11b8f8a). Ledger keys: `lmcap_ri|lmcap`, `lmcap_rand|lmcap`, `lmcap_perm|lmcap`, `qwen25vl_7b|ret_img`, `qwen25vl_7b|rand_d0_img`.
- `v4_gate`: every block-3 id carries `-b1` and records `batch_size: 1`, so no batched release is needed; OV-dev-B `at_` runs need the v1.2 nomination file of record (`c_attr_nomination.json`, sha `559c18c1…`, CC-363 ruling 1a), which exists.
- Labels and intervals: `pair`, `label`, `detected` (m = 1), one index matrix per set (`boot_idx`).

Missing (one scoring package, a new topic, as CC-346 ruling 5 made the 1b scoring):
1. A stage for block 3 in `c_attr_score.py`: copy `/root/outputs/c_attr_b3` read-only and check it against the logged sums (`SRC` knows only `c_attr` and `c_attr_b1`); the §7.1 parity gate; score both sets.
2. The rows: `set_rows` forms only `<model>|ret / rand_d / perm_p` estimands, so no LMCap τ_sel / τ_pair / τ_marg and no `ret_img − rand_d0_img` row is computed; `cmd_summary` would also refuse the LMCap rows (model names `lmcap_ri` … have no D1 record).
3. The D1 parity read from `STEP3_<runner>.json`; the E6 labels; the block-3 batch note; the K5 verdict line (LMCap τ_sel on OV-dev-B DETECTED or not, m = 1), written to its own result file and logged before any other block-3 row is read.
4. The reference files at scoring time only, as CC-362 ruled (§9 item 7); the stage-2 ledger `be716482…` for the parity gate.

## 9. What a FRESH host needs before launch (tonight's host was deleted at 15:47Z; nothing of it is reused)

1. **Machine.** One rented RTX 3090 / 3090 Ti 24 GB of the registered spec (the `running-rented-gpu-jobs` skill; CUDA ≥ 12.4, RAM ≥ 32 GB, disk ≥ 200 GB). Nothing else runs on it during block 3 (§6.7). `/root/.vsps_machine_id` = `h1` (the job accepts `h1`/`h2` only, and the isolation hook installs on those ids).
2. **Tree.** A sparse code-only clone at the committed HEAD in `/root/vsps`: `scripts/`, `manuscript/prereg/`, `rescap/`, `configs/` and the single tracked file `data/coco_probe/chair_synonyms.txt` (no other `data/` path). Check HEAD, `git diff --quiet`, every SUMS file.
3. **Venvs.** `/root/vsps/.venv` (CPU commands; numpy, scipy); `/root/venv-lb`, pip freeze sha256 `685ffe2a0100ce2489cccd77313d366fb1dce4455871a9d82f65aa139fa85784` (setup_gpu.sh `H_LB`); `/root/venv-t1` = python3.10 venv with the venv-lb freeze plus `open_clip_torch==2.32.0`, `ftfy==6.3.1`, `wcwidth==0.2.13`, installed `--no-deps` (c_t1 registry `venv` entry; OPS-1030n), pip freeze sha256 `1766dc23a71509ba4fb6b8adb34b1999a3a2bf78ebe1e227730fd6647bea3599` (checked by the job). The 45-line venv-t1 spec of record (`2cb23ab9`, OPS-1030n) was not located in the repo by this coder; building to the exact freeze sha is the likeliest fresh-host stall, so the operator builds it first and compares `pip freeze` line by line with the venv-lb freeze plus the three lines; a different sha is a STOP (no other environment is admitted without a judge line). For scoring later: Java (any; its version goes into `VERIFY.json`).
4. **Models** (`HF_HUB_OFFLINE=1` at run time; fetched before with the network on): `$NCS_DATA/models/qwen25vl_7b` by its B-N1 pins (setup_gpu.sh; `check_snapshot` in the decoder); with the network on and `HF_HUB_OFFLINE` unset, `/root/venv-lb/bin/python scripts/c_attr/c_attr.py fetch --model xglm_2_9b --snapshot $NCS_DATA/models/c_t1_xglm_2_9b`; the same for `mclip_h14` → `c_t1_mclip_h14`; `mkdir -p $NCS_DATA/models/c_t1_xlm_roberta_large` first, then `fetch --model xlm_roberta_large --snapshot $NCS_DATA/models/c_t1_xlm_roberta_large` (the files land in the HF hub cache, which `t1check` reads offline; only the `.c_t1_ok` marker goes into that directory). Each `fetch` checks every registry hash and writes `.c_t1_ok`. No HF token is needed (all three are ungated). InternVL3, Aya-Vision and SigLIP2 are not needed.
5. **Stored inputs** restored from the laptop backup to their host paths and checked by `STORED_SHA256`: `/root/outputs/c_stage1/emb.npz` (59e65f6f), `/root/outputs/c_stage2/emb_ov_dev_b.npz` (5ad23a67), `/root/outputs/c_stage2/emb_xm_dev500.npz` (48ec2476). For the later scoring only: the two Qwen2.5-VL stage-2 `zs` runs (5bf37a77, d11b8f8a), the six stage-2 OV-dev-B runs of the parity gate, the stage-2 ledger (`be716482…`).
6. **Data under `$NCS_DATA/datasets/`** (only the `ISO_DATASETS` names; nothing else there): `ktvic/train_data.json` (`72ee9b57…`) and `openviic/uit-openviic-annotation-train.json` (`d757520e…`), the memory captions; `c_t1_mem/memfiles_vi.json` (`886af149…`; if no copy of record is at hand, it is rebuilt on the host CPU by `c_attr.py memfiles --memory vi --c-lists manuscript/prereg/2026-10-22_c_stage1/lists.json --out …`, ids and hashes only, and must begin `886af149`). Images, **by list, into tmpfs** `/dev/shm/c_attr_b3/` and linked as `$NCS_DATA/datasets/openviic/images`, `ktvic/images`, `c_xm_dev500/images`: the 925 OV-dev-B files of `lists.json` `sets.ov_dev_b`; the 8,190 cluster representatives of `memfiles_vi.json` (KTVIC-train and OpenViIC-train first members); the 500 XM-dev500 files of `sets.xm_dev500` (alone in their folder: `check_folder` refuses any other file). About 9,615 files. Pushed with the skill's six-stream transport and arrival check (manifest sha, `sha256sum -c` silent, counts, no links inside). No test image, no OV-dev-A image needed, no archive left. The job's `memcheck` and every decode re-hash each image; gate b3.g5 runs the guard over the tmpfs root.
7. **Segmenter and reference files: scoring time only, not for the decode.** `$NCS_DATA/vncorenlp/VnCoreNLP-1.2.jar` sha256 `9e2811cdbc2ddfc71d04be5dc36e185c88dcd1ad4d5d69e4ff2e1369dccf7793` with its `models/wordsegmenter/` files (no committed pin; their sha256 go into `VERIFY.json`, the §7.1 parity gate binds; CC-348 R1). The two dev reference files as CC-362 ruled: copied unchanged from `.session_backup/2026-10-22/c_stage2/subsets/` to `$NCS_DATA/datasets/openviic/uit-openviic-annotation-dev.json` (`550cfe06b06084976e81286531f7f4e52bea717e29004c699ccaf1e48919bdff`) and `$NCS_DATA/datasets/c_xm_dev500/xm_dev500_data.json` (`0da82355b65ab284fe55fc0d3c4101090301767347a02721890556618ca4905f`), checked on the laptop and on the host, mode 444, never opened, never rebuilt, removed after the scoring pull (logged). No other reference file goes to the host.
8. **Host gates** b3.g0–g5 (§5), with the OWED records b3.g1, b3.g2, b3.g4, before call 1.
9. **Money and dates.** L-before of the skill (cap ≤ 12 GPU-h × rate + set-up); planning value as §3: call 1 by 2026-11-15T00:00Z (07:00 VN) keeps K5 and the K7 freeze (2026-11-16 12:00 VN) reachable.

## 10. Custody

Development sets only (OV-dev-B, XM-dev500); no test set is staged, decoded, scored or opened; the decoder refuses every test set by name, by file and through the open() hook. Captions, list files of shown examples, ledgers: never committed (binding 6). The comparators and the job print counts, ids, timings and hashes only; no caption string is printed anywhere. Reference files only at scoring time, as CC-362 (§9 item 7). No host name, IP or port in any repo file or LOG line.

## 11. Block-3 report (to the coordinator; Vietnam time from `date`)

One block: host gates b3.g0–g5 (with the OWED records now made); D1 per runner PASS/FAIL with identical counts; r_b, L_b, P3 and the cap as logged; the `lmcap_perm` list hashes; steps OK / NOT RUN; GPU-h used of the cap; pull verified; host kept for scoring or deleted. K5 is answered only by the scoring package.

## 12. Open for the judge (each with the recommended reading)

- **O1 Re-decodes not in §6.5 (changes the counts).** §6.5 decodes no `lmcap_ri` and no `ret_img` on OV-dev-B, so K5 and the image-format τ_sel there would pair stored C-T1 decodes (another host, `c_t1.py`, not in `STORED_SHA256`, under a path this coder may not open) with new decodes. Recommended: decode both again on the block-3 host (+1,850 captions, +1.19 GPU-h), V2's rule "all arms of one backbone × set come from one host" read into V8; the stored C-T1 rows stay out of block-3 contrasts. Alternative (not coded): pins of record from the C-T1 pull SUMS plus a 50-item host-parity check with fallback.
- **O2 D1 for LMCap.** LMCap has no `ret` arm; recommended: `lmcap_ri` on the first 50 OV-dev-B items, reversed then forward, 50/50.
- **O3 D1 for Qwen2.5-VL in block 3.** The registered D1 pair is on the text `ret` arm, which tests neither the image path (`rices_generate`) nor its rate (about 3.5 s vs 0.8 s). Recommended: D1 on `ret_img`; the text-arm D1 is not repeated.
- **O4 Drop order.** §6.5 registers none and V8 says "unchanged". Recommended: bottom-up in the run order of §2, with the K5 arms first (LMCap OV-dev-B dropped last).
- **O5 Cap terms.** P3 over the steps only; D1 seconds charged to the cap; 12 GPU-h ceiling during D1 (as 1b).
- **O6 "Batch size 1" for LMCap.** One image per `generate` call, beam 3 inside it. Recommended: counts as batch size 1 under V8; ids carry `-b1`.
- **O7 LMCap retries.** No partial file: a retry re-decodes the run from its first item (≤ 3 attempts under the cap). Recommended: accept; beam search without sampling is deterministic in principle, and D1 checks order invariance.
- **O8 Tier labels.** LMCap τ_sel on OV-dev-B is new (no `lmcap_rand` existed), but the stored `lmcap_ri` row was scored in C-T1 (ret − lmcap_ri contrasts seen). Recommended: K5 is a first look; LMCap τ_pair / τ_marg on OV-dev-B do NOT carry "split of a known τ_sel" (the sum is not known); the image-format τ_sel is a first look (its `ret_img` side was seen in C-T1). XM-dev500 rows: no rule (§7.8).
- **O9 Batch note.** V6's note names v1.2 and K1; recommended for block-3 rows: "batch size 1 (addendum v1.2 V8)".
- **O10 Pins of record with 8 hex only.** `memfiles_vi.json` 886af149, the two memory-caption annotations 72ee9b57 / d757520e: the full values are not in the repo; gate b3.g0 logs them and requires the prefixes.
- **O11 Images in tmpfs behind symlinks.** Allowed by the hook (it resolves paths; names are still refused), but the job's guard does not walk symlinked dirs; gate b3.g5 closes it.
- **O12 Scoring.** A separate package (§8), read as a new topic, before any block-3 score; recommended to write it while block 3 decodes.
- **O13 OWED records.** No self-test, mutant or dry-run record of the changed code exists (the host was deleted before they ran); b3.g1, b3.g2 and b3.g4 are STOP gates on the launch host, and a defect there goes back to the judge.

## 13. Block 2 (one paragraph; no package written)

Block 2 would need: `c_attr_registry.json` (v1.1 §11.1; not in the prereg folder, CC-363 ruling 6) with Gemma-3-4B's four null hashes filled from the Hub tree API (licence accepted, PI-1111h) and Idefics3 borrowed from `l1b_registry.json`; very likely a second pinned environment for Gemma-3 (Paper A's other-family arm needed one with torch 2.6 for Gemma-3-4B-it, commit 765c858), which the C-ATTR job and venv-lb do not provide; a `block2` job mode (smoke, the dev299 `zs` + Vietnamese check + 7 `ret` runs + host-side selection scoring in a scorer venv, D1 before 2.2, the 24 GPU-h cap), its own read, and about 10–14 GPU-h at unmeasured rates for two backbones. It could share block 3's host only in sequence (§6.7), at the price of delaying K5. The cut-off 2026-11-14 18:00 VN (11:00Z) is not realistic for two backbones: a package, read and commit by 11-13, a set-up of half a day and about 5–7 GPU-h per backbone leave no margin; one backbone (Idefics3, no new environment, but it may fail the Vietnamese check) is possible only if its package is read by 11-13 midday. Recommended: block 3 first on its own host; block 2's NOT RUN sentence stands unless its read is done by 2026-11-13 12:00 VN.
