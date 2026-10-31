# JUDGE_READ_REQUEST: VSPS-J E1+E2 prereg, one-judge read (REVERSIBLE, bar >= 90)

Requested 2026-10-31 by the drafting agent. Licence: CC-207 rulings 3-4 (one-judge reads for each later VSPS-J prereg).
Parent results: M0 anchored in commit f77eea1 (m0_result.json 0779d20d; few-shot DROP, detector CONTINUE).
A GO licenses the gatekeeper commit of the files below and one rented RTX 4090 block for E1b + E1a, under PI funding
(PI-1031i). No test set is touched.

## Files (sha256)
- `scripts/vsps_j_e1e2/e1e2.py` 8694206ee773214924f1435deb1ecce704ad9d29bc5e3c4a0cd6bb3aade50b05
- `scripts/vsps_j_e1e2/e1e2_job.sh` aedaf47f816201fde3b21f59c56544b4d6ab5ed3eedc483f5e74ba8d00ff9597
- `scripts/vsps_j_e1e2/ret.py` bf0c169621b9821a89068d66d4993b4a97258855c7332a0fc4a4dafb31a42941
- `scripts/vsps_j_e1e2/test_e1e2.py` 63fc3abf78a157a74d328a8c28d2d075cf47138106d7d083864a6f0304cac19f
- `scripts/vsps_j_e1e2/SHA256SUMS` fab66fb43a3c2509a600037a4b454a437586fdd690f56fe218c1afe3049451d2
- `manuscript/prereg/2026-10-31_vsps_j_e1e2/PREREG.md` 555a832f5ff46e51d1a1cbbef5d33b6946cb65b7cf29aa89a9d5dc61b8fa5bc4
- `manuscript/prereg/2026-10-31_vsps_j_e1e2/e1e2_plan.json` 0aafd39234305ff7e1a40a23969be9c44bb2e31cb96ffe3fb78565a2e55aa656
- `manuscript/prereg/2026-10-31_vsps_j_e1e2/SHA256SUMS` 9965d745a0a0b3624c697f10bacaff4f4c77a44ece760c8ed94ccf0de6e18b10
- `scripts/vsps_j_m0/m0.py` 5d3c02f414bd5743d437ec399e07431b4d38d970b16b901c52a9a657505ef7b2 (unchanged since dba7685, imported)

## Gatekeeper commit set (one commit, after a GO)
- `scripts/vsps_j_e1e2/{e1e2.py, e1e2_job.sh, ret.py, test_e1e2.py, SHA256SUMS}` at the shas above (no `__pycache__`).
- `manuscript/prereg/2026-10-31_vsps_j_e1e2/{PREREG.md, e1e2_plan.json, SHA256SUMS, JUDGE_READ_REQUEST.md}` and the
  ruling's diff if any. The fetch list is not committed.
- `manuscript/directions/PORTFOLIO_3Y_2026-10-29.md`, exactly one appended line, placed directly under the l.189 VSPS-J
  M0 line (the l.188 "Dev-only (spent)" block, the de facto spent and tier-2 ledger per CC-208a G1):
  `VSPS-J E1+E2 (dev-explore): E1a decodes all 231 UIT-ViIC test images (already spent; dev only; ids sha 96e6ffe9 in manuscript/prereg/2026-10-31_vsps_j_e1e2/e1e2_plan.json); E1b re-probes the 3,700 KTVIC train stage-1 images (in-sample). No new owner displaced; T-COCO from E1a is never a tier-3 claim.`
- No other PORTFOLIO byte changes. Pre-commit checks: both SUMS, selftest, `plan` byte-identical, 8-gram scan 0 on every
  committed file, ident grep 0.

## What to check (each re-runnable on the laptop)
1. `~/.venvs/vsps_j_m0/bin/python -I scripts/vsps_j_e1e2/e1e2.py selftest` -> `selftest ok`. `e1e2_job.sh --selftest`
   also needs `accelerate` and `qwen_vl_utils`, which the laptop venv lacks, so it runs only on the host.
2. `python3 -I scripts/vsps_j_e1e2/e1e2.py plan` rewrites `e1e2_plan.json` byte-identically. `e1e2.py fetchlist` rebuilds
   the E1a fetch list (231 lines, sha 993fa66e = the plan), which is not committed because the n-gram scan counts
   UIT-ViIC JSON fields.
   - 3,700 records, 192,216 propositions, 345,768 unique Vintern questions.
   - E1a overlaps all 0; 231/231 in instances_train2014.
3. `python3 -I scripts/vsps_j_e1e2/ret.py <extracted stage1 records>` -> 52.9 (4,474/8,453) and 69.6 (n 21,049)
   (CC-207 W9).
4. The construct uses `m0.py` unchanged (dba7685). `generate_stage1.py` and `verify.py` are unchanged; the side-log is a
   wrapper, checked on mock models in `test_sidelog_stage1`.
5. CPU dry run of `score_e1b` (synthetic P(yes) = yes-share of the recorded K=5 samples, no model output, deleted after): ran end to end in 27 min for 63 replays (the earlier one-pass rule). `recorded_v1` reproduced R 36.5 / P 41.1 / retention 52.9 / mirror 69.6, and `replay_v1_k5` reproduced H1's R0 (R 36.9 / P 41.2). Its base fell below the P floor, which is why the rule now has two passes. Its numbers are not evidence and are not reported.

## Questions (each with the recommended answer and the default)
1. **E1a cost and stop rule.**
   - The program's 1.5 h and "50 images > 3 h" came from the multi-stream fleet anchor. One GPU measures 85.7 s per image
     (3090, 3,700 records), so the estimate is 5.3-5.7 h.
   - Accept cap 7.5 h with the 20-image projection?
   - Recommended: YES. Default: YES.
2. **E1b fidelity gate.** Replace the program's "< 97 % of propositions agree" with coverage = 100 % and
   kappa(P(yes) >= 0.5, K=5 majority) >= 0.70 (gate T0.5 G2; anchor kappa 0.794)? Recommended: YES. Default: YES.
3. **Cross-family probes (program E2).** Defer them to an E2b amendment, because the repo has no second-family yes/no
   logit path and M0 did not trigger the pivot. Candidate: Aya-Vision-8B at the C-T1 pin. Recommended: DEFER.
   Default: DEFER.
4. **Selection rule.** Per-type S_hi through `per_type_thresholds`, two coordinate passes in a fixed type order, grid
   0.50-0.95, max retention at P >= 39.2, ties to the larger value. Selected on the in-sample 3,700 (W6 disclosure).
   Accept? Recommended: YES. Default: YES.
5. **Environment.**
   - Qwen is pinned to the B-N1 revision cc594898; the FAIR stage-1 revision was not recorded.
   - `accelerate` and `qwen_vl_utils` are recorded in `pip_freeze`, not version-pinned.
   - Attention is sdpa.
   - Accept with disclosure? Recommended: YES. Default: YES. The alternative, pinning exact versions, needs one more
     edit before launch.
6. **69 KTVIC train images with no records.** These are FAIR's pipeline-screening set (`data/screening/val_manifest.json`),
   not failed images. Excluded by construction; running them would mix pools and add about 1.6 h. Recommended: exclude.
   Default: exclude.
7. **Detector arm.** `e2_chosen_det` uses the H1 vote rule (no boxes, `absent_bbox_is_evidence` held at v1 True in
   every condition so the vote is the only difference) on laptop CPU and is descriptive only. The
   KTVIC-built map may cover few UIT-ViIC sports nouns; the coverage is reported. Recommended: keep it as descriptive.
   Default: keep.
8. **Funding.** One block, about 9.5-10.6 h of rental, about 145-185k VND (worst case at the caps about 235k VND).
   Recommended: fund after the GO. Default: no rental without the PI line.
9. **E1a image failures.** At most 11 (5 %) images may still fail after the one resume. They are listed and contribute 0
   T-COCO units; more than 11 makes the score INCOMPLETE. Recommended: YES. Default: YES.
10. **S_hi range limit.** V jumps from 0.25 to 0.75 at P(yes) = 0.5, so a claim with P(yes) < 0.5 has S <= 0.55 and
    can be SUPPORTED only at S_hi <= 0.55 with M and G both live and high. Accept this as the E2 construct (the knob
    mainly tightens), or add a polarity-cut knob? Recommended: accept for E2 and revisit in E2b. Default: accept.

## Default if no ruling
No commit and no rental. The CPU-side files stay drafts outside any commit.
