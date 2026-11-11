# C-ATTR-DEV block 1b: run document

Version v1.1 = v1 (sha256 `aab14580…`) + the text fixes R0–R7 of ruling CC-346, applied by script. v1 written 2026-11-11T17:55Z (2026-11-12 00:55 VN). Nothing in block 1b has run, and no block-1 output has been scored or opened. Label on every output file and row: `DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY`. AI opinion, not expert-validated.

Rule: `C_ATTR_DEV_ADDENDUM_v1_2.md` (sha256 `5858d69d…`, commit 99fa1fa, `SHA256SUMS_1B` `bc2e3f47…`) on registration v1.1 (`44f81329…`) and erratum 1; rulings CC-340 (ruling 4, V1–V10, W1–W5), CC-341 and CC-339 (host gate 0.2). Where this document and the addendum differ, the addendum binds. Run document v1.1 (`e12a1c6b…`) still governs everything this file does not change. Wording rules of run document v1.1 l.7 apply unchanged.

Code: `scripts/c_attr/` at the commit that holds `C_ATTR_1B.diff` (diff against 7e7471f) and the new `scripts/c_attr/SHA256SUMS`. Machine id `h1` (role H1, the host of block 1); models, images and stored runs are already there. Nothing on this page names a host address.

Deviation note (CC-346): block 1 ended by itself before this document was used: `JOB DONE` 2026-11-11T17:12:31Z, 6.41 GPU-h, all 41 registered steps OK, no CAP STOP; pulled, whole-tree digest equal to the host's, read-only (LOG OPS-1112c). Sections 0 and 1 are therefore moot and are not executed; no block-1 step is reported NOT RUN under V10, and the pulled copy is not pulled again.

## 0. Staging while block 1 still runs (CC-340 ruling 4)

1. `git -C /root/vsps fetch` only. **Do not** check out, edit or copy anything into `/root/vsps` while the block-1 job runs: bash reads `c_attr_job.sh` as it goes, and each step starts `c_attr.py` again.
2. Block 1 keeps running until steps 1–2 of §1 are ready. If it ends by itself first (`JOB DONE` or `CAP STOP`), skip §1 items 1–3 and pull as registered (run document v1.1 §8 item 1), without wiping the host.

## 1. Stop of block 1 (V10, W5), pull, verify, 444

1. Note the last `START` line of `/root/outputs/c_attr/logs/job.log`. That step and every later step are reported **NOT RUN ("stopped for block 1b, CC-340")**.
2. Stop the job first, then its decode. Order matters: a TERM to the decode alone makes the job count a failed attempt and start the step again.
   ```
   pkill -TERM -f 'c_attr_job.sh block1 '          # the job and its heartbeat subshell; the EXIT trap removes RUNNING
   pkill -TERM -f 'scripts/c_attr/c_attr.py decode' # timeout and the decode it runs
   ```
3. Before anything is hashed, all of these must hold: `pgrep -f scripts/c_attr` prints nothing; `nvidia-smi --query-compute-apps=pid --format=csv,noheader` is empty; `/root/outputs/c_attr/RUNNING` is gone. If RUNNING is still there, remove it by hand and log that as an OPS deviation. The `.partial` file of the stopped run is kept and never scored.
4. A killed job does not write its sums (job l.72), so the operator writes them with the same command and logs this as an OPS deviation:
   `cd /root/outputs/c_attr && find out logs parity -type f ! -name '*.partial*' | LC_ALL=C sort | xargs -r sha256sum > SHA256SUMS`
5. Pull `/root/outputs/c_attr/` to `.session_backup/machines/ATTR_H1/root/outputs/c_attr/`, run `sha256sum -c SHA256SUMS` there (all OK, counts equal), then `chmod -R a-w` (files 444). **The host is not wiped or deleted:** block 1b runs there, and D1 needs the step-1.0 (b) files in `/root/outputs/c_attr/out/`. All of this happens before any 1b command. No 1b job runs beside block 1 (§6.7). The job refuses while `/root/outputs/c_attr/RUNNING` exists, and on h1 it also refuses while `/root/outputs/c_attr/SHA256SUMS` is missing.

## 2. Code and host gates (before any 1b decode)

Only after the code read GO (CC-340 W1) and the gatekeeper commit. Then `git -C /root/vsps checkout <HEAD>`. Check HEAD, `git diff --quiet`, `scripts/c_attr/SHA256SUMS`, registration `SHA256SUMS` and `SHA256SUMS_1B`. All from `/root/vsps`, with `C=/root/outputs/c_attr_checks_1b; mkdir -p $C`, in the job's environment (`HF_HUB_OFFLINE=1`, `NCS_DATA=/root/ncs-data`). Each row is a STOP gate: a non-zero rc, a SURVIVED mutant or a JOB STOP in the dry run ends the session before any 1b decode. The fix is then made on the laptop and goes through a new code read and a new push. CPU only, not charged to the cap.

| # | check | command | gate |
|---|---|---|---|
| 1b.g0 | step-1.0 verdict files (CC-341 W2) | `sha256sum /root/outputs/c_attr/parity/STEP10_*.json > $C/step10.sha256` | the three values equal, in full, the 64-hex values of the addendum's values table; one OPS line quotes them; otherwise STOP |
| 1b.g1 | self-tests | `for f in c_attr c_attr_lists c_attr_score; do /root/vsps/.venv/bin/python -I -B scripts/c_attr/$f.py --selftest; done > $C/selftest.log 2>&1; /root/venv-lb/bin/python -I -B scripts/c_attr/c_attr.py --selftest >> $C/selftest.log 2>&1; sha256sum $C/selftest.log > $C/selftest.log.sha256` | rc 0; four "selftest ok" lines. The c_attr line names the v1.2 ids / D1 / plan cases; the c_attr_score line names the v1.2 gates |
| 1b.g2 | mutants | `/root/vsps/.venv/bin/python -I -B scripts/c_attr/c_attr_mutants.py --no-netns --jobs 4 > $C/mutants.log 2>&1; sha256sum $C/mutants.log > $C/mutants.log.sha256` | control passes, then "33/33 killed; survived: none". `--no-netns` is new in this diff (CC-339 W3): it drops the `unshare -rn` wrapper that this container refuses. The self-tests are offline anyway (`HF_HUB_OFFLINE=1`). If the code read does not accept `--no-netns`, the mutant run for the changed files is **OWED**: it can then run only on a host that allows user namespaces. Block 1b does not start while it is owed (CC-340 W1). |
| 1b.g3 | list sidecar | `(cd scripts/c_attr && sha256sum -c c_attr_lists.json.sha256) > $C/k0.log 2>&1` | "OK", `8a2b977f…` |
| 1b.g4 | dry run | `C_ATTR_DRY=1 bash scripts/c_attr/c_attr_job.sh block1b <HEAD>` (outputs under `/root/outputs/c_attr_b1_dry`), then `cat /root/outputs/c_attr_b1_dry/logs/*.log > $C/dryrun_logs.txt; sha256sum $C/dryrun_logs.txt > $C/dryrun.sha256` | `grep -c 'JOB DONE'` = 1, `grep -c 'JOB STOP'` = 0, `grep -c '^DRY at_'` = 56 (3 reversed decodes, because the dry ids carry `-smoke` and so find no step-1.0 file; 3 D1; 50 steps), `grep -c 'STEP 1b.0 .* D1 PASS'` = 3, `grep -c '^PLAN 1b:'` = 1 (the plan.log line; job.log repeats it after a time stamp), reading `P 12.76 GPU-h (Tier A 5.62), cap 19.13 GPU-h, 50 runs, NOT RUN none, Tier-A stop False` (§6.1 point rates, no load term); otherwise STOP |

## 3. Block 1b on H1 (tmux, from `/root/vsps`)

```
bash scripts/c_attr/c_attr_job.sh block1b <HEAD>     # call 1: preflight, 1b.0 D1, plan, PAUSE
bash scripts/c_attr/c_attr_job.sh block1b <HEAD>     # call 2, after the LOG line: Tier A, B, C at batch size 1
```

- **1b.0 D1 (V3), 150 captions.** For each backbone the job decodes the first 50 OV-dev-B `ret` items in the stored order at batch size 1 (`--redecode fwd50 --batch1`, run id `…-mvi-b1-fwd50`). It then compares them as strings with this host's step-1.0 (b) decode `/root/outputs/c_attr/out/…-mvi-rev50.preds.json`, via `compare --d1`. That command refuses any other reference (by run id and batch size) and prints counts and failing ids only. The verdict goes to `parity/STEP1B0_<model>.json`. A D1 FAIL takes that backbone out of the 1b families, and its 1b steps are NOT RUN. No re-registration is made for that failure.
- **Plan (V7).** `plan1b` reads the model-load seconds and decode seconds that each D1 decode records separately (`timing`). It computes P = Σ_b [N_b r_b + n_runs_b L_b] / 3600 over the steps of the passing backbones and sets the hard cap to min(40, 1.5 P) GPU-h. It writes `CAP_1B.json` and `STEPS_1B.tsv`. If 1.5 P_A exceeds the cap, or would end later than 2026-11-15 12:00 VN, the job STOPs before Tier A (JOB STOP; back to the judge). D1 seconds count against the cap.
- **PAUSE.** Call 1 ends with `PAUSE after D1 …` and the sha256 of `CAP_1B.json`. The coordinator then writes one LOG line before call 2: the D1 verdicts (PASS or FAIL and the identical count of each `parity/D1_<model>.json`), the `old_sha256` of each `D1_<model>.json` (on h1 equal to that rev50 file's line in the pulled block-1 `SHA256SUMS`, hash lines only; on h2 equal to the `.sha256` sidecar of its own rev50 decode; otherwise STOP), r_b and L_b, P, P_A and the cap, the `CAP_1B.json` sha, and the latest start of call 2 (2026-11-15T05:00Z minus 1.5 P_A; a later start is a STOP before Tier A). A D1 decode that needed more than one attempt (a `START D1_<model>` line with attempt 2 or 3) under-counts its decode seconds: STOP before call 2, back to the judge. Call 2 writes `STEP1B0_*.json` and `D1_*.json` again with a new time stamp, so their sha256 are logged from the final pull; a verdict there that differs from this line is a STOP before any score. `CAP_1B.json` is never deleted or made again after this linewithout a judge line. Call 2 re-runs the cheap comparators, skips the finished D1 decodes (`.done`), and reads the cap from the file.
- **Steps (V5), in this order, every run id with `-b1`, outputs in `/root/outputs/c_attr_b1/out/`:** Tier A: Qwen2.5-VL, then InternVL3 (τ = −∞). OV-dev-A `ret`, `rand` d0, `perm` p1, p2; OV-dev-B `ret`, `rand` d0–d2, `perm` p1, p2 (18,388 captions). Tier B: Aya-Vision OV-dev-B, the same six arms; then `zs` OV-dev-B for all three (8,325). Tier C: XM-dev500, all three: `zs`, `ret`, `rand` d0–d2, `perm` p1, p2 (10,500). Total 37,213 + 150. A cap stop is final and every later step is NOT RUN, so the cap drops Tier C first, then the Tier B `zs` runs, then Aya-Vision's Tier B arms. Tier A is never run in part (plan rule above). A failed step resumes from its partial file, at most 3 attempts, then JOB STOP. K7 (2026-11-16 12:00 VN): every unfinished step NOT RUN. A CAP STOP, a JOB STOP or K7 before the last Tier-A step is OK leaves Tier A in part: no 1b output is scored until a judge line. No other job runs on the host while `/root/outputs/c_attr_b1/RUNNING` exists (v1.1 §6.7; CC-338 N2), except CPU-only checks of another paper under `nice -n 19`, never during call 1, each logged as an OPS deviation with its start and end (CC-346 ruling 6).
- **Second host (addendum, last table row; CC-341).** Only a host of the registered specification (1× RTX 3090 / 3090 Ti 24 GB), machine id `h2`, set up as in run document v1.1 §3. It needs no step-1.0 files. One backbone moves there with all of its 1b steps: `C_ATTR_1B_MODELS=<backbone> bash scripts/c_attr/c_attr_job.sh block1b <HEAD>` on h2, and `C_ATTR_1B_MODELS="<the other two>"` on H1. The job's D1 on h2 is a batch-1 reversed decode followed by the batch-1 forward decode (100 captions, counted in the cap). Each host plans its own backbones and runs its own Tier-A deadline test. The one hard cap of V7 covers both hosts. The code sets each host's cap from its own P, and those two caps add up to min(40, 1.5 P) only while 1.5 P ≤ 40. The split is fixed before H1's call 1 (`C_ATTR_1B_MODELS` on both hosts); a split made later needs a judge line. Call 2 on the second host runs only after both cap lines are logged and cap_h1 + cap_h2 ≤ 40 GPU-h; otherwise its steps are NOT RUN and the matter goes to the judge. A D1 failure on either host removes that backbone on both hosts.

## 4. Monitoring

Only these may be read while the job runs: `logs/job.log` lines (START / OK / FAIL / CAP STOP / JOB STOP / STEP 1b.0 / PLAN / PAUSE), the age of `HEARTBEAT`, `gpu_seconds.tsv` and return codes. No caption, no per-image score, no partial file.

## 5. Pull, verify, 444

After `JOB DONE` or `CAP STOP` and `RUNNING` gone: pull `/root/outputs/c_attr_b1/` and `/root/outputs/c_attr_checks_1b/` to `.session_backup/machines/ATTR_H1/root/outputs/`. Check a whole-tree digest equal to the host's, and run `sha256sum -c SHA256SUMS` in `c_attr_b1/`: every line OK except `logs/job.log`, which the job appends to after writing its sums (as in OPS-1112c). `CAP_1B.json` and `STEPS_1B.tsv` lie outside `SHA256SUMS`: log their sha256 (`CAP_1B.json` equal to the PAUSE line). Then `chmod -R a-w`. Then wipe and delete the host (logged), L-after. A second host is handled the same way, under `ATTR_H2`.

## 6. Scoring: not licensed here

This document runs no scoring command. Scoring waits for the scoring run document of CC-338 S1 and for S3 and S5. When it comes, the order of V4 binds, and the code enforces it:

1. **Batch-1 OV-dev-A.** Score the batch-1 OV-dev-A runs of Qwen2.5-VL and InternVL3. Then `nominate` writes `c_attr_nomination.json`; it reads `-b1` rows only and refuses once any new OV-dev-B row exists. Its sha256 goes to the LOG.
2. **Batch-1 OV-dev-B.** `score` refuses every OV-dev-B `at_` run without that file. It refuses `c_attr_nomination_v11.json` by name and by content. Then `summary --parity <STEP10_*.json> <STEP1B0_*.json>` produces the verdict file, and its sha256 goes to the LOG. In that file, batch-1 rows need a D1 PASS. Batched and stored rows sit in their own `batched` section with no family and the label "A1 not met; batched decode; descriptive", plus "base arms re-decoded on the new host" where host parity failed.
3. **Batched output.** Only then may any batched block-1 output be scored (`score --verdict <that file>`). Release clause: if 1b ends with no verdict, `nominate --closed "<reason>"` writes the empty v1.2 file, the OPS line "1b closed: <reason>" logs its hash, and `score --nomination <that file>` then opens gate (3). The code cannot see the LOG lines; the coordinator checks them.

## 7. Block-1b report (to the coordinator; Vietnam time from `date`)

One block. Block 1: the step stopped and the steps NOT RUN, and the pull (n files, SHA256SUMS OK, OPS deviation for the operator-written sums). Host gates 1b.g1–g4. D1 per backbone, PASS or FAIL. P, P_A and the cap as logged. Steps OK or NOT RUN. GPU-h used of the cap. Pull verified. Host deleted.
