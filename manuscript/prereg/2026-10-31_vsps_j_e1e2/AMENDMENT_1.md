# VSPS-J E1+E2 AMENDMENT_1: split hosts (E1b rented 4090, E1a M1 only), E1a's own smoke, staged scoring

Status: DRAFT for the CC-209a one-judge diff read (REVERSIBLE, bar >= 90), 2026-10-31. Not committed.
Parent: PREREG.md as committed in 43423d9 (CC-209 W5; PREREG 555a832f). Licence: CC-209 path (ii), W1 and W2.
Funding: **PI-1031k** (LOG 2026-10-31T12:33Z, standing PI approval to rent once a judge-approved job needs it; tell the
PI what was rented at rent time). PREREG l.5-6 cites PI-1031i for funding; that line is about year-1 scope and says
nothing about renting. This is disclosed here, not edited in the PREREG (CC-209 r14).
Nothing below changes a rule, threshold, grid, seed, SESOI, cap, statistic or the plan (section A9).

## A1. Hosts (CC-209 r1, W1a)
- **E1b: one rented RTX 4090.**
  - It holds only KTVIC train images (the 3,700 records' files), the pinned records tarball and Vintern.
  - It never fetches, stages or holds any UIT-ViIC file. It never fetches Qwen.
  - `e1e2_job.sh e1b` has no UIT-ViIC or Qwen step.
  - The host is deleted after the pull (PI-1031c).
- **E1a: M1 only,** the only host that may hold test images, spent ones included.
  - Queue: behind A-T3 tier 3 and MT4 K1+K6 tier 1 (CC-207 r8). It moves earlier only if the PI opens an idle M1 window
    (CC-209 Q3). VSPS-J slips; A, B and C never do.
  - Cost: about 6-7 M1 GPU-h: cap 7.5, the 3090 anchor of 85.7 s per image is native there, plus the Qwen download.
    M1 is already rented, so there is no new rental.
- **E1a stays in its own folders (W6):**
  - its own `HF_HOME`. The job refuses without one, because `refs/main` is rewritten to the pins and other owners'
    jobs must never see that;
  - its own venv, OUT, STAGE, UIT_IMAGES and KT_SMOKE folders.
  - It never touches `/root/a_t3_m3`, MT4 or C staging, or other owners' datasets.
  - It is excluded from the 30-min backup pull, as `a_t3_m3` is.

## A2. E1a runs its own smoke (W1b; replaces PREREG section 6 "refuses unless the E1b smoke passed, same block")
- Before Qwen loads, `e1a` runs the section 6 smoke with the rules unchanged:
  - the same 100 items: the first 20 images of the seeded KTVIC-train order, 5 questions each (`e1e2.py smokelist`);
  - the same thresholds: tokens, finite, median mass >= 0.5, text >= 90 %, `yes_no_logit` equivalence |dP| <= 1e-3.
- It writes `OUT/e1a/smoke.json`. A fault writes the STOP marker (rc 2), and `m0.refuse_if_stopped` refuses any resume.
- Only those 20 KTVIC **train** images are staged on M1 for it (`KT_SMOKE`). Their bytes are checked against
  exclusion.json `ktvic_test` (FAULT on a match, as in E1b).
- The smoke is inside E1a's cap clock: `launch.json` t0 is written before it.

## A3. One OUT folder per host block (W1c; amends CC-208a G2 for this block)
- `OUT_E1b` on the rental and `OUT_E1a` on M1. Each is named in its own launch OPS line, and only those two folders may
  ever be scored.
- A second folder for the same sub-job, or a relaunch after any STOP, is a breach that needs an amendment.
- **Pull:**
  - a sha256 manifest of every file in the folder, written on the host;
  - scp to a new laptop folder; `sha256sum -c` against that manifest.
  - The pull OPS line lists every file with its sha, including `pip_freeze_<sub>.txt` and the presence or absence of
    STOP and of the projection records.
- **Score root on the laptop:** a new folder holding `e1b/` copied from the E1b pull and `e1a/` copied from the E1a pull.
  Each copy is re-checked against its host manifest before `score`.

## A4. Environment (W1d, CC-209 r11)
- **Both sub-jobs:** the M0 pins, unchanged (torch 2.15.0, torchvision 0.29.2, transformers 4.51.3, numpy 2.5.4,
  pillow 13.0.0, timm 1.0.30, einops 0.8.2).
- **E1a also:** `accelerate==1.15.0` and `qwen-vl-utils==0.0.14`, asserted exactly by the job.
  - These are the versions used with transformers 4.51.3 in the M2 venv of 2026-10-18 (`.session_backup/2026-10-18/
    gpu_jobs/M2_STATUS.md` and the M2 venv freeze).
  - The E1b assertion does not require them.
- **Attention is sdpa.** flash-attn is not installed.
- **Qwen at the B-N1 pin cc594898,** disclosed: the FAIR revision is unknown, and E1a is never compared with the 3,700.

## A5. Scoring (W2): staged, with the S_hi vector frozen before E1a
- **Staged form (primary, fixed now), used when E1b is pulled before E1a launches:**
  - `e1e2.py score --stage e1b --out <score root> --res <root>/e1b_result.json`, once, as soon as E1b is pulled.
  - That result holds the fidelity gate, the full sweep trace and the chosen S_hi vector, or E2-KT STOP.
  - Its sha goes into an OPS line **before** the E1a launch.
  - After the E1a pull: `score --stage e1a --frozen <root>/e1b_result.json --frozen-sha <logged sha> --res
    <root>/e1a_result.json`, once. The E1a read uses only that frozen vector, so S_hi is fixed before any E1a datum
    exists.
- **Fallback, only if E1a launches before E1b is pulled:** `score --stage all`, once, after both pulls.
- **Never:**
  - `score` refuses to overwrite an existing result file;
  - `--stage e1a` refuses a frozen file whose sha differs from the one given;
  - no partial score is repeated, and the form is not switched once one result file exists.

## A6. Operator rules (CC-209 W6, r5, r15)
- An E1a FAILURES exit (rc 5, no marker) may resume once, with an OPS line. A second resume is a breach.
- A deleted and recreated sub-job folder would reset its own cap clock, so recreating one is a breach.
- **Laptop detect step (CC-209 r13 / W4 form):**
  - the 231 images are re-fetched into a dedicated directory used only for `detect`;
  - they are deleted right after `detect`;
  - the deletion is logged with the count and the sha of the sha list.
- **PI notice at rent time:** rental id and price in the next report (PI-1031k).

## A7. Cost (replaces PREREG section 5 block totals)

| sub-job | host | estimate | cap | money |
|---|---|---|---|---|
| E1b | rented 4090 | about 0.7 h setup + 2.95-3.86 h (345,768 × 0.0307 s median / 0.0402 s mean) | 5.0 h | about 3.7-4.6 h ≈ **60-80k VND**; worst case (5 + 1 h) ≈ 105k VND |
| E1a | M1 | 5.3-5.7 h + Qwen and Vintern download | 7.5 h | none new (M1 already rented) |
| detect, score | laptop CPU | about 1.7 h + about 1 h | none | 0 |

## A8. Disclosures carried from CC-209 (no PREREG edit)
- **Selection rule:** the two-pass rule is "a design revision on in-sample dev, before any real logit" (r10).
- **Retention gain:** most of any retention gain comes from the change of answer source (`logit_base` vs
  `replay_v1_k5`), not from the S_hi knob. Every write-up says so (r16).
- **W25:** not run for E1a (r6), the M0 exception extended, read-only. The 231 stay in exclusion.json for every later
  W25 pass.
- **M0:** the M0 block held 91 spent Karpathy-test images on a rental without a custody ruling. Disclosed, not a
  precedent (r1).

## A9. Unchanged, byte-equal to 43423d9
- **`e1e2_plan.json` 0aafd392**, and with it:
  - the seeds;
  - the E1b order (e2a3bcaa);
  - the E1a order (b3dee1a8);
  - the fetch-list sha (993fa66e).
- **`ret.py`.**
- **Every e1e2.py function the E1b pass, E2 replay or T-COCO read uses:** `run_pass`, `run_smoke`, `replay`,
  `kt_metrics`, `select_s_hi`, `tcoco_*`, `cluster_ci`, `fidelity`, `score_e1b`, `score_e1a`, `install_sidelog`,
  `run_stage1`.
- **Every constant:** caps, projections, grid, passes, P floor, retention stop, DR margin, n_absent, kappa, B.
- **Imported code, unchanged since dba7685:** `scripts/vsps_j_m0`, `scripts/vsps_h1`, `generate_stage1.py`,
  `verify.py`.

## A10. The diff (`CC209a_W1.diff`, against 43423d9)
- **`e1e2.py`:**
  - `cmd_e1a`: the E1b-smoke dependency is replaced by `e1a_smoke()` (A2), and `m0.check_model` is kept;
  - new `cmd_smokelist`;
  - `cmd_score` gets `--stage {all,e1b,e1a}`, `--frozen`, `--frozen-sha` and a no-overwrite refusal (A5);
  - argparse additions; docstring lines.
- **`e1e2_job.sh`:**
  - a sub-job selector (`--selftest | e1b | e1a`), with E1b free of UIT-ViIC and Qwen (A1);
  - E1a requires `HF_HOME` and `KT_SMOKE`, and asserts the A4 pins;
  - `pip_freeze_<sub>.txt`.
- **`test_e1e2.py`:**
  - staged scoring: refused repeat, refused wrong sha, frozen e1a stage;
  - `broken()` now fails by RuntimeError as intended (CC-209 W1e).
- **SUMS:**
  - scripts SUMS: the e1e2.py, e1e2_job.sh and test_e1e2.py lines;
  - prereg SUMS: the PREREG.md line, plus the new AMENDMENT_1.md line.
- **`PREREG.md`:** only a 3-line amendment pointer under the title.
