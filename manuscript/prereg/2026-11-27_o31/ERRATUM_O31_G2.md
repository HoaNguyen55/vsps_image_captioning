# ERRATUM O31-G2 to ERRATUM_O31_2.md (817eac8f) and COMPUTE_PLAN_O31_v3.md (7557ca3b): the batch and the cap of the InternVL3 probe pass G2

Written by ruling CC-534 (2026-11-28) after the first launch of G2 stopped with no output. It is committed before G2 is launched again, and while no output of G2 exists.
It changes no hypothesis, threshold, margin, seed, set, grid, gate, estimand, statistic, family, probe form, score, token set, question form, model, revision or environment. It changes one run setting (the batch of the InternVL3 probes) and one cap (the cap of G2), and it states why neither can favour any hypothesis.

[COORDINATOR: state at commit, by record: the first launch of G2 (2026-11-28T15:05:42Z; launch.json t0 15:05:59Z) ended with exit 1 at about 15:34:58Z (g2.log mtime) by an out-of-memory error in the batch-8 parity phase (operator records 20261128T153529Z_B50_exit_diag a2fa0b87 and 20261128T153528Z_B50_g2_poll f50dab35; gate after PASS dd2bc040; LOG OPS-1128dg-o31-g2-oom); read by the coordinator on the test computer at 2026-11-28T16:36:03Z: the G2 folder holds launch.json 784b84358aa1edcafe1ff8c334ae36ec8065e38005db68a934cc4b05eba6019d, inputs.json 0650be7e4f891a218ef5cc95db075401c1e1601986f76926c546d6e0788e90c1 and model.json 902995c54113bf7ccd8228d32f16667770213c0e0c7461dfd993f79870e05806 and nothing else (no smoke.json, shard, .partial or STOP.json); no G2 or other study process runs and the only GPU process is the desktop session's remote-desktop service; no G3 folder or file exists; P1 has not run. ERRATUM_O31_7 was committed (6bd3e17, 2026-11-28T16:10:26Z) after this text was written and before this commit; it does not change the G2 batch rule or cap, and "E7" in this erratum names section E7 of ERRATUM_O31_2 (how caps are counted), not ERRATUM_O31_7.]

**Why.**
- G2 was launched on 2026-11-28 at 15:05:42Z on the investigator's PC, which has one RTX 3090 with 24 GB (ERRATUM_O31_2 E1). The t0 of its launch.json is 2026-11-28T15:05:59Z.
- The job first probed the 50 images that E4 names at batch 1. These were 2,428 probes, held in memory and never written. It then began the batch-8 pass that E4 compares with batch 1.
- By its image size, the second image of the job is cut into 13 tiles (12 tiles and the thumbnail, about 3,370 tokens per sequence); the size of the failed allocation agrees with this. At its first batch of eight probes, the model's output layer asked for 7.62 GiB, to hold the scores of every position of the eight sequences. At that moment the job already held 16.72 GiB, and the card has 23.56 GiB in total. The job ended with an out-of-memory error at about 15:34:58Z. It wrote no smoke.json, no shard and no probe row.
- This is not chance. The same images in the same order give the same batches, and 16.72 + 7.62 = 24.34 GiB is more than the whole card. On this GPU, the batch-8 pass cannot be computed for an image cut into 13 tiles that has eight or more questions. In the G2 pool there are about 1,088 such images of 3,752 (an estimate from the image sizes; the failing batch itself is in the job's log). The condition that E4 sets for batch 8 ("every probe's s at batch 8 is within 1e-3 of its value at batch 1") therefore cannot be established on the registered hardware. In every other case, E4 names batch 1.
- The batch-8 check in the host self-test's smoke used five images with four questions each. It never formed a batch of more than four sequences, so it could not show this.
- The first launch probed at about 0.70 s per probe at batch 1 (2,428 probes in about 28.5 minutes after the model was loaded). COMPUTE_PLAN v3 planned 0.47 s per probe, from an earlier run whose prompts had a median length of 1,845 tokens. The G2 prompts have a mean length of about 2,180 tokens, weighted by probes (an estimate from the image sizes). At the measured speed, the 175,215 probes of G2 need about 34 hours, which is more than the cap of 30 hours.

## G2-1. Batch of the InternVL3 probes (replaces the second bullet of ERRATUM_O31_2 E4)

- Every InternVL3 probe job of O31 runs at batch 1, with one question per forward pass. This covers G2 and the V-COCO probe jobs that run through the same code: G3v at tier 1, and the V-COCO probes of T2 and T3. The batch-8 pass and the batch-8 parity check of E4 are not run.
- The job's smoke.json records the smoke check of §4.1 and "batch": 1. It has no "parity" entry. As E4 says, the decision holds for the whole job.
- Vintern-1B probes stay at batch 1 (E4, first bullet). G2 stays one job over every pool image with records (E4, third bullet).

**Why this cannot favour any hypothesis.**
- Under E4, batch 1 gives the reference values. Batch 8 was allowed only where it agrees with batch 1, within 1e-3 and on the top token. Running at batch 1 gives exactly those reference values.
- This rule is fixed before any probe value of G2 has been written or read. The batch-1 values of the first launch were held in memory only, and they were lost with the process.
- This rule does not use the five-image record of the host self-test (3 of 20 probes outside 1e-3, at batches of four).

## G2-2. The cap of G2 (replaces the G2 cap of COMPUTE_PLAN v3 §1, 30 h)

- The cap of G2 is 48 hours of wall time from the t0 of its launch.json (2026-11-28T15:05:59Z). It is counted as ERRATUM_O31_2 E7 counts every cap, so the first launch, the wait for this erratum and any later pause or restart are included. G2 therefore stops under K4 if it has not ended by 2026-11-30T15:05:59Z.
- G2 is launched again only if the launch starts before 2026-11-28T23:05:59Z (t0 + 8 h). If it cannot start by then, it goes to a ruling.
- Basis, fixed now:
  - 175,215 probes at 0.70 s take about 34 h;
  - the first 50 images are probed again for the smoke check, about 0.5 h more;
  - with a relaunch within 8 h of t0, the expected end is at most t0 + 42.5 h, and the cap leaves at least 5.5 h (about 16 %) for a slower speed;
  - with a relaunch within 3 h of t0, it leaves about 10.5 h (about 30 %, close to the margin of 1.3 used for the caps of COMPUTE_PLAN).
- The planning value of G2 becomes about 35 GPU-hours (it was 23). The 0.48 hours of the first launch count in the cap of G2 and in the study's GPU total.
- This erratum does not change the caps of the other InternVL3 probe jobs (G3v, T2, T3). The ruling that clears each of those launches checks its cap against the measured speed, before that job's first output.

**Why this cannot favour any hypothesis.**
- A cap decides only whether the registered work is completed. It does not choose among probe values.
- The cap is set from the speed of the first launch, before any probe value of G2 exists. That speed is a property of the hardware and of the prompt lengths.

## G2-3. Code

- probe.py: the InternVL3 entry of FAMILIES gets "batch": (1,) and "cap_h": 48.0, and the docstring's line on the batch says so. No line that computes a score, writes a shard or checks the cap clock changes.
- The line for probe.py in PROTECTED_071c8dc.sha256 changes, with a note in PROTECTED_NOTE.txt. The tests and mutants named in ruling CC-534 are added.
- G1's Vintern probes ran at batch 1 with the earlier probe.py (commit b1b693b). The Vintern path is unchanged, so they are not affected.

## G2-4. Paper

The paper's run record carries this sentence:
"The InternVL3-8B probes ran one question at a time (batch 1): the registered rule allowed batches of eight only after a check against batch 1 on the first 50 images, that check could not be computed on our 24 GB GPU because its first full batch of eight long image sequences ran out of memory before any score was written, and a correction registered before any InternVL3 probe output fixed batch 1, the reference setting of that rule, and raised the compute cap of this step from 30 to 48 hours to match the measured speed."

## G2-5. Text left as it was

- ERRATUM_O31_5 (E-D.1) lists "The G2 probe form, environment and batch rule" as text that it leaves as it was. This erratum changes the batch rule only. The probe form and the environment stay.
- Everything else in the prereg, ERRATUM_O31_1 to ERRATUM_O31_6 and COMPUTE_PLAN v3 is unchanged. This includes E7 (how caps are counted), K4 and every other cap.
