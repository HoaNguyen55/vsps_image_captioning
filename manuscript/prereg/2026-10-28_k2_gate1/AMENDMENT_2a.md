# K2 Gate 1 rule, amendment 2a (DRAFT, filled): venv-gd re-pin after the M1 rebuild

**Status:** filled 2026-10-29 under CC-162 ruling 4 / W6, after `setup_gpu.sh` with `WITH_K2=1` stopped on M1 at its venv-gd check (HEAD d2011245; log `.session_backup/machines/M1/m1_rebuild_2026-10-29_rerun.log` l.33, 07:20:56Z):
- recorded 5291fc30…;
- observed **696f7dc31a3d6de537d772a3f53f8b0a7db8ac2bc77af08ded8e4eeaaee16ef5**.

The cause is GroundingDINO's unpinned `requirements.txt`: the resolve drifted. It binds after a one-judge diff read and the gatekeeper's commit. No GPU step, no K2 restore and no Gate 1 output came before it.

## Change

| Place | Old | New |
|---|---|---|
| `scripts/k2_gate1/k2_gate1_job.sh` l.14 `H_GD=` | 5291fc308f4457cbc313431d73827e6bb5890c6534eb6177087d6720ff181cab | 696f7dc31a3d6de537d772a3f53f8b0a7db8ac2bc77af08ded8e4eeaaee16ef5 |
| `.session_backup/machines/setup_gpu.sh` l.54 `H_GD=` (beside the repo; sha e68b8532 → c1c9661c) | the same | the same new value |
| freeze text | none was kept on M3 (setup l.54, old comment) | `scripts/k2_gate1/venv_gd_freeze.txt` (new; 61 lines) |

**The freeze text, reproducible:**
- `venv_gd_freeze.txt` is the byte output of `/root/venv-gd/bin/python -m pip freeze` on M1, fetched on 2026-10-29 over the configured ssh alias. No host is written here.
- Its file sha256 is 696f7dc3…. It equals the hash computed the way setup and the job compute it (`pip freeze | sha256sum`), and the value setup printed.
- The file is pinned in both K2 `SHA256SUMS` copies.

## Superseded RULE lines (RULE.md bytes unchanged)

- l.49, "run on the UT pool in venv-gd (freeze 5291fc30)": the detector pass ran on M3 with 5291fc30. On M1, venv-gd only passes the job's freeze, `pip check` and `imports --venv gd` checks, now against 696f7dc3.
- l.126, the venv-gd pin in the CPU checks: now 696f7dc3.

## Why the drift cannot change Gate 1 inputs

- The detector step is done. `detect.json` (03acf723…, 2,392 images) was produced on M3 with venv-gd 5291fc30.
- It is reused only through `detect.done`, whose sha matches (Amendment 2 §4 and the restore manifest). The job skips the step; it is not re-run.
- `targets.json` (d25473f2…), which feeds every arm, was built from that `detect.json` and is reused by sha.
- No remaining Gate 1 step imports venv-gd for computation. The remaining steps are train_det, train_ref and the five val decodes, all in venv-q3.

## Package versions: what can be compared

- `detect.json`'s `pins` recorded only these items, and every one is the same on M1:
  - gd_commit 856dde20…;
  - torch 2.5.1+cu121;
  - cuda 12.1;
  - transformers 4.44.2;
  - the model file shas (unchanged; checked by `k2_p2_detect.py fetch`).
- The M3 build log (`gd_build2.log`) adds torchvision 0.20.1+cu121, also the same on M1.
- **Differences that can be shown: 0 of the 5 recorded versions.**
- The other packages of the M3 venv were never recorded (no freeze text was kept, and the build logs list no versions). So which of the 61 M1 packages differ from M3 is **unknown and cannot be listed**. That gap is why the freeze text is now committed.
- For the record, M1's freeze lists numpy 2.2.6, opencv-python 5.0.0.93, timm 1.0.30, supervision 0.31.3, pycocotools 2.0.11, addict 2.4.0 and yapf 0.43.0, with GroundingDINO as an editable install at 856dde20.

## Checks and procedure

1. Done on the laptop:
   - `bash -n` on the job and on setup_gpu.sh;
   - `k2_gate1_job.sh --selftest` rc 0;
   - `sha256sum -c scripts/k2_gate1/SHA256SUMS` all OK;
   - both SUMS copies identical.
2. One-judge diff read of `.session_backup/2026-10-29/k2_2a.patch`, then the gatekeeper's commit.
3. Rerun `setup_gpu.sh WITH_K2=1` in full (CC-162 ruling 4). It must finish with no mismatch, including:
   - `k2_p2_detect.py --selftest` and `k2_gate1.py imports --venv gd` in the rebuilt venv;
   - `pip check` clean;
   - a clean `/root/GroundingDINO` at 856dde20;
   - the `_C` build at arch 8.6.
4. Then G4 (`k2_gate1_job.sh --selftest` on M1), and only then the Amendment 2 §8 restore.

A venv-q3 or venv-lb mismatch is not covered here: it is a FAULT → PI.

## Disclosure (RULE §10)

"venv-gd was rebuilt on M1 with a different freeze (696f7dc3); GroundingDINO's requirements are unpinned. The detector output had been produced on M3 with 5291fc30 and was reused by sha; no detector pass ran on M1. The recorded versions (torch, CUDA, torchvision, transformers, GroundingDINO commit, model files) are identical; the other package versions of the M3 environment were not recorded."
