# B-F1 run record: the single KTVIC test decode on M3

- **Authority:** CC-070 (GO, 92%), from `.session_backup/2026-10-13/decisions/CC-070.txt`.
- **Runs:** one. No retry and no re-launch.
- **Scoring:** not done here. The coordinator scores locally from the committed scorer.
- **Predictions:** nobody opened or printed a prediction file. Every check used only exit codes, presence, sizes, counts, sha256 and provenance fields.

## Machine and code
- **Machine:** M3, machine_id `O-2326839`. GPU: one NVIDIA GeForce RTX 3090 (24576 MiB), driver 595.104.02. `check.json` recorded the same machine_id and card, and all three provenances carry them.
- **Code:** the decode ran from a clean git bundle of the registered commit `0c7fa0bf9bf4271ee00eec3ffd780fcba551b332` (branch paper-v10). git_dirty was false in all three provenances.
- **Gates:** G-1 file `g1_gate_O-2326839_v2.json` (sha256 5d45aa3e…), with `G1_GATE_ENFORCED_OK` before START.
- **Packages:** python 3.10.12, torch 2.5.1+cu121, transformers 4.51.3, peft 0.21.2, trl 0.19.1, numpy 2.2.6, pyjnius 1.7.0, py_vncorenlp 0.1.4, pycocoevalcap 1.2. The full freeze is in `pip_freeze.txt` (7332d343…).
- **Package note (judge's wording):** "numpy 2.2.6 and pyjnius 1.7.0 differ from the gate environment and are not pinned by the registration; peft 0.21.2 equals the prereg value." peft was installed through a constraints file at that value.
- **Supplement line (CC-070 b):** "The decode ran from a clean git bundle of the registered commit; packages the registration does not pin may differ from the gate environment (run record)."

## Timeline (UTC) and exit codes
| event | time | result |
|---|---|---|
| job queued (`cp` into `/root/queue/01_b_f1_ktvic_test_decode.sh`, `cmp` OK) | 12:31:59 | rc 0 |
| qrun: G-1 enforced, START | 12:33:59 | G1_GATE_ENFORCED_OK |
| `score_b_f1.py check` | 12:34:13 | PASS (failed []) |
| p1dev_s42 decode + stamp | 12:43:18 / 12:43:19 | rc 0 |
| p1dev_s43 decode + stamp | 12:52:27 / 12:52:28 | rc 0 |
| p1dev_s44 decode + stamp | 13:01:35 / 13:01:36 | rc 0 |
| SHA256SUMS written; qrun logs `OK 01_b_f1_ktvic_test_decode` | 13:01:36 | job rc 0 |

- The job took 27.6 min in total.
- The evaluate.py logs contain 0 Traceback or Error lines. This was a count only; the logs were not read.
- After the job, the qrun tmux session was stopped, so nothing can run a second time. `/root/queue` holds no job; the job file is in done/.

## Provenance (all three)
| member | n_predictions (= keys) | preds_mtime_utc | adapter_sha256 | base_revision | job_sha256 | view_sha256 | evaluate / scorer |
|---|---|---|---|---|---|---|---|
| p1dev_s42 | 558 | 12:43:18Z | 227a3312… | cc594898… | e85fdc66… | 79dbae58… | a68d5682… / 9c57cc97… |
| p1dev_s43 | 558 | 12:52:27Z | d74d3dd4… | cc594898… | e85fdc66… | 79dbae58… | a68d5682… / 9c57cc97… |
| p1dev_s44 | 558 | 13:01:35Z | b04354c8… | cc594898… | e85fdc66… | 79dbae58… | a68d5682… / 9c57cc97… |

job_sha256 e85fdc66… equals the addendum's pin of the job file.

## Output files
- **M3 path:** `/root/outputs/b_f1_ktvic_test/`
- **Local mirror:** `.session_backup/machines/M3/root/outputs/b_f1_ktvic_test/`. This follows the S1 precedent of `.session_backup/machines/O-2308423/root/outputs/t3_2_s1_seed_consensus`.
- **Mirror check:** all 14 entries of `sha256sum -c SHA256SUMS` are OK locally, and the 3 sidecars are OK. SHA256SUMS itself is 742e1570d8da56f83b6fc20172d4fccb91a752138c87af9c6ade578fd16073f5 on both M3 and local.
- **Queue logs:** mirrored to `.session_backup/machines/M3/root/queue/`.

| file | sha256 |
|---|---|
| check.json | d169f716467fe20d18c3d05e7714da92eb16a8c9dc6a655c26b294fcca82a00d |
| ktvic_test_images_only.json | 79dbae58424a350cd05665bbf533ac6add523e22ecae549ce9de3eff5caa2d1e |
| p1dev_s42-test-short.log | 778566f66abfc61ec5276bf94bb7b6f2f24ac0767e41822705923e8578c5effd |
| p1dev_s42-test-short.preds.json | 40ee7846728ee3735ac300b21fa3aa810466c51357131ced9bf10e6d7878fec4 |
| p1dev_s42-test-short.preds.json.sha256 | b24b1424fe27430e658aa6fefbe77a87559b095cfa4ba7003a1637c4e2194d70 |
| p1dev_s42-test-short.provenance.json | ccc22749173efaad6bb05b1ed3c8a5a1462706d2dc6dce19027ae3a21936e5dc |
| p1dev_s43-test-short.log | b50040b66733e856b3ab204506d5de023e02edfa55fe2fb66a475be3ee23e968 |
| p1dev_s43-test-short.preds.json | b8d347677e961128228692faab5100b169feb5da3c4d9e346e85862c602dbc2f |
| p1dev_s43-test-short.preds.json.sha256 | b5bb0d70a4c9096d33823fe2b50d3c63425fd8ee58a20ab5c733ef9814adcf95 |
| p1dev_s43-test-short.provenance.json | f21dfaf502241cf3b6bb8277a894ec18030770882e9c5a4fb88b68e9a7e0669b |
| p1dev_s44-test-short.log | 0cd70d761a0e2b7f969b4cec0ee354daef8ef0d38b8246f15991086f381d532c |
| p1dev_s44-test-short.preds.json | 3de831742f2a23ab559a3dddfdd127dab31c378044a2e324bac84636c0d9b6ee |
| p1dev_s44-test-short.preds.json.sha256 | 5c759bec6906035204c7b10378ec5ada71bfa4f48705eebc0ae3798a6bb017a5 |
| p1dev_s44-test-short.provenance.json | 4daddfce67ccef667f9e557941a3e39c2dc3a9f299ee0cd7b924faf14316aa5e |
| SHA256SUMS | 742e1570d8da56f83b6fc20172d4fccb91a752138c87af9c6ade578fd16073f5 |

`check.json` is byte-identical to the pre-go dry run `claude_ops/check_dry_M3.json`. That is expected: the checks are deterministic on the same machine and inputs, and both files record the same machine_id and card.

## Scoring (not run here)
This is registration procedure step 4, run once from the committed scorer at HEAD (records.run = `data/results/b_f1/b_f1_run.json`, which does not exist yet):
```
NCS_DATA=<local dir holding datasets/ktvic> VNCORENLP_DIR=<VnCoreNLP dir, jar 9e2811cd…, rdr 9e62f96b…> JAVA_HOME=<JDK> \
  python scripts/b_f1/score_b_f1.py run data/results/b_f1/b_f1_run.json \
  --gate manuscript/prereg/2026-10-20_b_f1_record/b_f1_gate.json \
  --outputs .session_backup/machines/M3/root/outputs/b_f1_ktvic_test
```
- `B_F1_STAGE` must be unset.
- Run it from the repo root with the committed scorer.

## Scoring (local, 2026-10-21)

- **Attempt 1 failed in the environment, before anything was read.** It ran under the system python3 3.12.3 and stopped at `score_b_f1.py:705`, in `env()`, with `PackageNotFoundError: pycocoevalcap`. In the scorer, `env()` runs before `run()` (`:711`), so no prediction was read and nothing was scored, and no output file was written. The log is `score_attempt1.log`. The judge ruled it not a look (CC-070b).
- **Attempt 2 (CC-070b) ran once, from the committed scorer, at 13:38–13:39Z.**
  - Environment: a fresh venv pinned to the gate environment (python 3.12.3, numpy 2.5.4, pycocoevalcap 1.2, py_vncorenlp 0.1.4, pyjnius 1.9.0), with VnCoreNLP jar 9e2811cd, rdr 9e62f96b and `JAVA_TOOL_OPTIONS=-XX:ActiveProcessorCount=1`.
  - Before running, `env()` was asserted equal to the committed gate's env block.
  - py_vncorenlp 0.1.4 exists on PyPI only as an sdist (pure Python), so it was built from that sdist.
  - Inputs: the mirrored outputs, with SHA256SUMS 742e1570.
  - Result: exit 0. The output is `data/results/b_f1/b_f1_run.json` (sha256 998e4f33). The verdict is **FAIL**: D_MBR −0.391 [−2.437, 1.666]; dCHAIRi +0.103, inside its interval. The log is `score_attempt2.log`.
- **Independent verification.** A fresh re-run in the same pinned environment produced a byte-identical output, and the verdict rule was re-applied (`manuscript/verification/paperB/B_F1_run_verify.json`, d36e6ed5).
