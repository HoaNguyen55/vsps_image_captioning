# Judge read request CC-208a: VSPS-J M0, diff read of the CC-208 W1 fix (one judge, REVERSIBLE, bar >= 90)

Draft, not committed. This file and `CC208a_W1.diff` sit outside both SUMS.
- **Parent:** CC-208 (GO-with-fixes 91, gated). It requires the W1 code guard, then this diff read, before the
  gatekeeper commit and before any rental.
- **Scope:** CPU only. No GPU, no test set, no commit.

## Diff

`manuscript/prereg/2026-10-31_vsps_j_m0/CC208a_W1.diff`, 253 lines, sha256
765b2a76856ed9d6629e0ec887b886e47f22e72cc1a730b3364bca6d2ea688cd.
- Unified diff, `patch -p1`, of the five files that changed.
- Applied to the CC-208 bytes, it reproduces the new bytes exactly; `cmp` was checked for all five.

| file | CC-208 sha256 (old) | new sha256 |
|---|---|---|
| scripts/vsps_j_m0/m0.py | 9f81f899a658ee2e42a0fba73876a610ba28c5953487aaa531b53f9149577181 | 5d3c02f414bd5743d437ec399e07431b4d38d970b16b901c52a9a657505ef7b2 |
| scripts/vsps_j_m0/test_m0.py | 1e40ac16922f0085404b31c3be5864e4ee42b99ec4e42ec8110a79e8d9aefc16 | 3a80acc3d194d21e3f67c7a4d9bd27f2f52193f5ec0fbb4ed20abf347cfc1d93 |
| scripts/vsps_j_m0/SHA256SUMS | d7704e871d598e1c8bced70916060a9bc20ea0861ac900c10435b3d42686ecb9 | 0a6a964c4e66f0cfbe380901d9cba1533e2bc788575a7faa97a5a84dd4f5e7c7 |
| manuscript/prereg/2026-10-31_vsps_j_m0/PREREG.md | 53af5f6bc52977824655eba8a74cf2eff4d2b00d14f7f9f52b3ad38d645b33f4 | f0895bbf566daee59290a02533aeb9ce40f51daa7076b1614047fe30f90e4fac |
| manuscript/prereg/2026-10-31_vsps_j_m0/SHA256SUMS | 1b1c9a7e346e5e6eb00cac95ef059d3b3d4a25303502753903efeb79fb2b1324 | af456d525dc98457397e241d24d02cbc7d5dc7b8555c9546b129af84c72b6535 |

**Unchanged, byte-identical to the CC-208 shas:**
- `m0_stats.py` 60042806, `m0_job.sh` be5c6fce;
- `m0_plan.json` c422efd1;
- `dev_touched_ids.txt` 91db7e2f, `val_ids.txt` b4d4f35a, `train_ids.txt` 4a4033a5;
- `karpathy_test_val_ids.txt` 88e40e3c, `selection_excluded_ids.txt` 57195c49, `dropped_ids.txt` 41306bdb;
- `fetch_images.txt` 7f148c8e.

The prereg SUMS changes only on the `PREREG.md` line. The scripts SUMS changes only on the `m0.py` and `test_m0.py`
lines. `m0_job.sh` was not needed for the marker.

## What W1 changed (m0.py)

Changes by CC-208 W1 item:
- **a. Refuse at entry.** New `stop_reasons` / `refuse_if_stopped`. `cmd_probe` calls it right after `--out` is created,
  before the model loads, and `run_val` calls it at entry. It refuses on any of:
  - the `STOP` marker;
  - `smoke.json` `fault: true`;
  - `projection_pre_val.json` or `projection.json` `stop: true`.
- **b. Every non-zero exit writes the marker.** New `halt(out, rc, reason, n_img)` writes `STOP` (rc, reason, time,
  n_img) on:
  - the smoke FAULT (2);
  - the non-finite P(yes) FAULT (2; the row is flushed first);
  - the pre-val PROJECTION_STOP (3);
  - the 50-image PROJECTION_STOP (3);
  - CAP_STOP (4).
- **c. Cap before each image.** CAP_STOP is now checked at the top of the image loop, before decoding. The after-image
  check is removed.
- **d. Score guard.** New `check_scorable`, used by `cmd_score`. It refuses on a stop record or marker, on a missing or
  mismatched `probes.jsonl.sha256`, and on any non-finite `p_yes`.
- **Crash resume:** a crash or disconnect with no marker and no stop record still resumes.
- **Unchanged:**
  - `probe()` and `run_smoke()` (checked by `diff` of those functions);
  - the decision rule, thresholds, seeds, demos, plan, id lists and statistics.

**test_m0.py.** New `stop_cases()`, run inside the selftest with a fake probe (no weights) on the real plan order:
- the CC-208 simulation: pre-val stop (rc 3, marker), then the same call is REFUSED with 0 probes decoded;
- the same with the marker deleted is still REFUSED, because of the stop record;
- CAP_STOP before image 1 on a resumed run (rc 4, n_img 1, 0 probes);
- `smoke.json` fault is REFUSED;
- a crash with no marker resumes to DONE (1,537 new probes after 1 pre-existing row);
- score accepts the sealed clean run;
- score REFUSES on a sha mismatch, on a NaN row (even when resealed), and after a marker.

**PREREG.md.** Exactly one sentence was appended in 7.2 (the marker and refusals) and one in 7.3 (the CPU smoke ran on
m0.py 9f81f899; the W1 guard changed m0.py after it, with `probe` / `run_smoke` unchanged). No other byte changed; see
the diff.

## Results (laptop, CPU)

- `~/.venvs/vsps_j_m0/bin/python -I scripts/vsps_j_m0/test_m0.py` passes and prints `selftest ok`. The expected stop
  messages print on the way: PROJECTION_STOP, then CAP_STOP before image 1, then DONE, then the CAP_STOP test.
- `PY=~/.venvs/vsps_j_m0/bin/python bash scripts/vsps_j_m0/m0_job.sh --selftest` passes: SUMS, env pins and selftest.
- **Your simulation, replayed** on an untouched copy of scratchpad `m0sim/out` (`m0sim_replay/out`):
  - `projection_pre_val.json` sha 687b07ea, stop true;
  - `probes.jsonl` 30 lines, sha b73cfc50.

  Results:
  - `run_val` with the same arguments: `REFUSED: run stopped (projection_pre_val.json stop: true); amend, never resume`,
    with 0 probes decoded;
  - `check_scorable`: the same REFUSED;
  - the CLI `m0.py probe --out <copy>`: REFUSED (exit 1) before the model loads.

  `probes.jsonl` still has 30 lines afterwards. The original `m0sim/` was not modified.
- 8-gram scan of `PREREG.md`, `CC208a_W1.diff`, `m0.py`, `test_m0.py` and both SUMS: 0 (PASS).
- No e-mail address, host, IP or port in any file.
- aislop: 0 errors; 1 style warning (m0.py is 652 lines; CC-208 r11 says non-blocking).

## Please rule on

1. Does the diff implement CC-208 W1 a-e fully, and change nothing else (the decision rule, statistics, plan, id lists,
   probe path)?
2. Are the two PREREG sentences within the CC-208 W2 allowance?

## For the gatekeeper commit (CC-208 W3, binding, same commit)

**PORTFOLIO** (`manuscript/directions/PORTFOLIO_3Y_2026-10-29.md`, under the image-level rule l.185). Append exactly:

> VSPS-J M0 dev-touched: every M-HalDetect image, 786 val + 2,695 train = 3,454 COCO ids (27 in both; 73 never decoded), `manuscript/prereg/2026-10-31_vsps_j_m0/dev_touched_ids.txt` sha 91db7e2f. B4 drops them from restval (599 val + 2,027 train in restval). W25 not run for M0 (CC-208 r8); later W25 passes include these 3,454 ids.

**Tier-2 (spent, dev-confirm) ledger.** Append exactly:

> VSPS-J M0 probes 91 Karpathy-test images (M-HalDetect val ∩ Karpathy test) at dev only; held out of every operating-point choice; `karpathy_test_val_ids.txt` sha 88e40e3c.

**Commit set:**
- `scripts/vsps_j_m0/` (4 files + SHA256SUMS) at the new shas;
- `manuscript/prereg/2026-10-31_vsps_j_m0/` (PREREG.md, m0_plan.json, 7 id lists, SHA256SUMS);
- `JUDGE_READ_REQUEST.md` and this file;
- `CC208a_W1.diff` as an audit record outside the SUMS.

## Optional (CC-208 W5): corrected program lines

For the program owner; `manuscript/directions/VSPS_J_PROGRAM_2026-10-31.md` sha 1840f896 was not edited.
- **l.179 old:** "M-HalDetect val, all 3,200 descriptions (full split)."
  **New:** "M-HalDetect val (A-N3 pin 2cbc7942): 3,164 records / 786 images / 16,450 eligible spans; 769 images are
  probed after the pre-fixed UT-2,532 drop (see `manuscript/prereg/2026-10-31_vsps_j_m0/PREREG.md` sections 2-3)."
- **l.192 old:** "fetch M-HalDetect (public repo, licence check, no personal e-mail in any request);"
  **New:** "reuse the A-N3 pin `.session_backup/2026-10-19/HL_human_labels/dl_mhaldetect/` (val 2cbc7942, train
  03b088d1, CC BY-NC 4.0); no re-fetch (CC-207 W3; M0 PREREG section 2);"
- **l.214 old:** "(`VinternAdapter.yes_no_logit` exists, never run);"
  **New:** "(`VinternAdapter.yes_no_logit`, already run by `scripts/gate_t05.py` on 600 Vietnamese probes,
  `data/results/gate_t05.json`, 0.413 s/probe; never run on English spans or 2-shot prompts before M0, see M0 PREREG
  sections 4 and 8);"
- **l.402 old:** "**M0-cpu** yardstick on the laptop (M-HalDetect fetch, id overlaps, segment table, scorer + selftest)"
  **New:** "**M0-cpu** yardstick on the laptop (A-N3 pin reused, no fetch; id overlaps; scorer + selftest; done as
  `scripts/vsps_j_m0/` and `manuscript/prereg/2026-10-31_vsps_j_m0/`, CC-208)"

## Re-runnable checks

```
cd /mnt/d/vsps_image_captioning
(cd scripts/vsps_j_m0 && sha256sum -c SHA256SUMS)
(cd manuscript/prereg/2026-10-31_vsps_j_m0 && sha256sum -c SHA256SUMS)
~/.venvs/vsps_j_m0/bin/python -I scripts/vsps_j_m0/test_m0.py
PY=~/.venvs/vsps_j_m0/bin/python bash scripts/vsps_j_m0/m0_job.sh --selftest
# diff reproduces the new bytes from the CC-208 bytes (pre-fix copies kept in scratchpad cc208a_base/):
#   copy cc208a_base/{m0.py,test_m0.py,SCRIPTS_SHA256SUMS->SHA256SUMS,PREREG.md,PREREG_SHA256SUMS->SHA256SUMS}
#   into a scratch tree, `patch -p1 < CC208a_W1.diff`, then `cmp` against the repo files
python3 /tmp/claude-1000/-mnt-d-vsps-image-captioning/5a363495-c9d6-40f3-8f9c-a7285ef7a0e6/scratchpad/ngram_scan_cen.py <file>
```

Replay of the CC-208 simulation:
- `cp -r scratchpad/m0sim scratchpad/<new>`;
- call `m0.run_val(ad, val, img, (), smoke, <new>/out)` with a fake probe, then `m0.check_scorable(<new>/out)`;
- both must print REFUSED.

## Default if no ruling

No commit and no rental.
