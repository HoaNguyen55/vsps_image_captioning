# C-ATTR-DEV block 3 (the positive control): scoring run document v1, on the rented host

Version v1, written 2026-11-12T22:05Z (05:05 VN, 2026-11-13), from `date -u`. Not committed. Nothing in it has run. No block-3 output exists or was opened. Label on every output file and row: `DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY`. AI opinion, not expert-validated. Nothing on this page names a host address.

This is the scoring package that CC-368 ruling 12 ordered: block-3 run document v1.1 (`e8ae45a5…`) §8 items 1–4, plus CC-368 N4 and N5. It is read as a new topic. **No block-3 output is opened, and no stage below runs, before this package has a GO** (CC-368 ruling 12). The binding rules are:
- registration v1.1 (`44f81329…`) §7.1, §7.3, §7.4, §7.8, §7.10, §7.12, §10.1 (K5, K7) and binding 1;
- erratum 1 (`f9f0842e…`) E1, E2, E6;
- addendum v1.2 (`5858d69d…`) V3, V4 (1), V8;
- block-3 run document v1.1 §2, §4, §7, §8, §10;
- rulings CC-362 (the reference files), CC-363 (how the first scoring records were read) and CC-368 (rulings 3, 6 and 12; O1, O8, O9; N1, N4).

Where this document and those texts differ, those texts bind. Every reading this document makes is listed in §8 for the judge.

## 1. Code

| item | sha256 |
|---|---|
| `scripts/c_attr/SHA256SUMS` (the same 8 lines, the same order) | `886aaf636212369c2e8307785acc5b803ba19cef751618f67d08f1f7673d8ece` |
| `scripts/c_attr/c_attr_score.py` | `cca5e3270a4699672b06f1580d08af265dc55b447cd3b241233d6ec8611d99c0` |
| `scripts/c_attr/c_attr_mutants.py` | `082a0d307daf219920743f3427469f444bb3d4a888a2aa6136a43f111298bb53` |
| `scripts/c_attr/c_attr_score_job.sh` | `2515c73313688556a5ca65110be902672b66d3e8a687a960beca97c697a58d98` |
| unchanged and byte-equal to HEAD `60358b2`: `c_attr.py` a3bd7b93, `c_attr_job.sh` d367f3c6, `c_attr_lists.py` 494a0e56, `dryrun.sh` 3dce71cc, `STORED_SHA256` b12030dc | as in SHA256SUMS |
| `scripts/c_attr/C_ATTR_B3SCORE.diff` (= `git diff HEAD -- scripts/c_attr` at `60358b2`; 4 files, +429 / −13) | `1dc1a1c02a577dc89535a76f9b91a6a81f74e1dfb3f3977b0f7edbd8a6768c06` |

**What the diff does (the decode code is not touched).**
- **`c_attr_score.py`: three new stages.** `b3verify`, then `b3k5`, then `b3rest`. They are chained by `--prev` through the existing `cmd_stage`, so each stage runs once, the logged sha256 of the previous file is required, and the environment must equal the one recorded at verify. They run in their own work folder, `/root/c_attr_score_b3`, and every one is refused at and after K7 (`k7_open`).
  - `b3verify` does not score any block-3 output. It runs, in order:
    - the RUNNING refusal;
    - the test-set name refusal over the output tree and the pinned inputs;
    - `freeze_copy` and `tree_ok` of `/root/outputs/c_attr_b3` against the logged sums;
    - the pins (`b3_pins`): the two reference files, the nomination file and the two stored Qwen2.5-VL `zs` runs;
    - `env_record`;
    - the D1 verdicts from `parity/STEP3_*.json` (the existing `parity()`);
    - the §7.1 parity gate. This is the existing code, moved into `parity_7_1`, which 1b `verify` now calls too.
  - `b3k5`: K5 first (§3).
  - `b3rest`: the other registered rows.
  - Rows come from the new `b3_rows`. It reuses `pair`, `detected` (m = 1) and `label`, and does **not** call `apply_labels`, because that function stamps "split of a known τ_sel" on OV-dev-B τ_pair and τ_marg, which CC-368 O8 forbids here.
  - Scoring goes through the frozen `c_attr.cmd_score` (`score_call`), so the V4 gates (SC1) still bind.
  - Run ids come from the decoder's own `lmcap_run_id` and `run_id_of` (`b3_id`).
- **`c_attr_score_job.sh`.** `/root/outputs/c_attr_b3/RUNNING` is added to the refusal loop, and the block-3 stages log under `/root/c_attr_score_b3/logs/`.
- **`c_attr_mutants.py`.** 24 new mutants, B11–B34, all on `c_attr_score.py`. Each pattern occurs exactly once in the final bytes: checked with `grep -o -F … | wc -l` for all 24 new patterns and all 57 old S patterns.

## 2. Preconditions (each a STOP gate)

| item | check | otherwise |
|---|---|---|
| package read | a judge GO on this document, the diff and the build note (new topic), then one gatekeeper commit H_S of exactly the files in §1 plus this document and the build note | no stage |
| K7 | `date -u` earlier than `2026-11-16T05:00:00Z`; the code refuses every block-3 stage at and after that instant | K5 and every row NOT RUN (§6) |
| decode ended | `/root/outputs/c_attr_b3/RUNNING` is absent; `logs/job.log` ends with `JOB DONE` or `CAP STOP`; the done line of CC-368 ruling 10 is logged | no stage |
| decode pull | the block-3 run doc §7 pull is verified: the whole-tree digest is equal, `sha256sum -c` gives all OK except `logs/job.log`, mode 444. The OPS line gives the sha256 of `c_attr_b3/SHA256SUMS` (= **B3SUMS**). `CAP_3.json` equals the PAUSE line | STOP |
| D1 verdicts | the re-written `parity/STEP3_lmcap.json` and `STEP3_qwen25vl_7b.json` (D1 field only) equal the cap line of CC-368 ruling 10 (block-3 run doc §4: "a verdict there that differs from this line is a STOP before any score") | STOP, to the judge |
| K5 arms | if the LMCap D1 is PASS, job.log holds both `OK B3_lmcap_ov_dev_b_ri` and `OK B3_lmcap_ov_dev_b_rand` (step names; their outputs are `at_lmcap-ri_ov_dev_b-mvi-b1` and `at_lmcap-rand_ov_dev_b-mvi-b1`). If either is NOT RUN (a CAP STOP or JOB STOP before step 2), K5 is NOT RUN and no block-3 row is scored until a judge line (run doc §4). The code refuses too (`b3k5`) | STOP |
| code on the host | `/root/vsps` stays at `60358b2` and clean until the decode job has ended. Only then is H_S checked out there (`git fetch`, then `git checkout H_S`; `git diff --quiet HEAD`; `(cd scripts/c_attr && sha256sum -c SHA256SUMS)` gives 8 × OK). For the alternative place of the owed records, see §8 P8 | STOP |

## 3. The K5 rule as coded

- **Rule.** LMCap τ_sel = `lmcap_ri` − `lmcap_rand` on OV-dev-B. It is DETECTED iff θ̂ ≥ +2.0 and p ≤ 0.025, with m = 1. The sources are:
  - the registration v1.1 §7.4 DETECTED row (l.283) and §7.10 (l.347);
  - §10.1 K5 (l.417) and §7.12 (l.362);
  - erratum E1 and E2;
  - the CC-368 pilot checklist (l.264–265) and ruling 6.
- **The statistic.** p = (1 + #{b : bootstrap mean_b ≤ 0}) / 2,001 over the set's one index matrix, `default_rng(0).integers(0, 925, (2000, 925))` (§7.3, `c_attr.boot_idx`). Both bounds are inclusive.
- **Code.** `k5_verdict(row)` returns `"DETECTED" if detected({"k5": (row["d"], row["p"])}) else "NOT DETECTED"`, and `NOT RUN` when there is no row. The row's §7.4 label (DETECTED / REVERSED / NEGLIGIBLE / UNRESOLVED) is printed beside it.
- **What `b3k5` scores.** Only the two K5 arms: one `score` call, which writes 4 ledger rows (plain and masked3 for each arm). Nothing else of block 3 is read or computed. It writes `res/K5.json`, which holds:
  - the label and the registration;
  - the rule text;
  - the D1 verdicts;
  - the row (d, lo, hi, lo90, hi90, p, label, tier, E6 wording, the N1 and O9 notes);
  - the verdict and its consequence;
  - the input shas.
- **Consequences, fixed in the code (`K5_OUT`).**

  | verdict | consequence |
  |---|---|
  | DETECTED | "K5 not fired" |
  | NOT DETECTED | "K5 fired: the positive control failed; the word 'test' is dropped; third-party rows are printed without interpretation (v1.1 §10.1, §7.12)" |
  | NOT RUN | "K5 NOT RUN: the CC-363 ruling 5 line stands (no 'test': the positive control was not run); third-party rows are printed without interpretation (CC-368 ruling 6)" |

- **When K5 is NOT RUN.** With the LMCap D1 not PASS, `b3k5` writes `K5.json` with verdict NOT RUN and the reason "LMCap D1 not PASS…", and scores nothing (run doc §2). With the D1 PASS but a K5 arm missing, it refuses and writes no file (run doc §4).
- **Tier of the K5 row (CC-368 O8).** "K5 positive control (v1.1 §7.10, §10.1): first look at the contrast; the lmcap_ri level was seen in C-T1 (ret - lmcap_ri)".

## 4. Rows of `b3rest` (all m = 1, labels of §7.4; nothing else is computed)

| set | row | arms | tier string |
|---|---|---|---|
| OV-dev-B | `lmcap\|tau_sel` (read back from the K5 ledger; it must equal `K5.json` in d, p and label, otherwise REFUSED) | `lmcap_ri` − `lmcap_rand` | as §3 |
| OV-dev-B | `lmcap\|tau_pair` | `lmcap_ri` − `lmcap_perm` | "first look (not a split of a known τ_sel: the sum was not known)" |
| OV-dev-B | `lmcap\|tau_marg` | `lmcap_perm` − `lmcap_rand` | the same |
| OV-dev-B | `qwen25vl_7b\|tau_sel_img` | `ret_img` − `rand_img` d0 | "first look; its ret_img side was seen in C-T1" |
| XM-dev500 | the same four rows | the same | "no rule (v1.1 §7.8)" |

- **On every row:**
  - `wording`: E6. LMCap rows carry "re-implementation of the LMCap recipe by this study; not the authors' code (no licence); not a statement about the published numbers". The Qwen2.5-VL rows carry "image-caption-pair prompt format, as used by RAGCap; not RAGCap".
  - `decodes`: "all arms decoded on one host in block 3; stored decodes not used (CC-368)" (N1).
  - `batch`: "batch size 1 (addendum v1.2 V8)" (O9).
  - `tag`: the label.
- **No "split of a known τ_sel"** appears on any block-3 row (O8).
- **The Qwen2.5-VL rows** also carry `beside`, a pointer to the text-only batch-1 τ_sel of the same backbone and set (§7.10 "beside"). For OV-dev-B that is `VERDICT.json :: sets.ov_dev_b.rows.qwen25vl_7b|tau_sel` (a69a0ec2…); for XM-dev500 it is `SUMMARY.json :: sets.xm_dev500.rows.qwen25vl_7b|tau_sel` (1d78cd20…). No difference row is computed.
- **K5 not DETECTED or NOT RUN.** Every row then carries `interpretation`: "printed without interpretation (K5 not DETECTED)", taken mechanically from `K5.json`.
- **Runners.** Only a runner with a D1 PASS in `STEP3_<runner>.json` is scored. A block-3 run of a runner without one is refused (V3, V8).
- **Absent rows.** A row whose two arms are not both present (a step NOT RUN) is absent and listed in `not_run`. Rows come from full sets only (925 or 500 images; otherwise refused).
- **Unregistered rows.** None is computed: no masked3 contrast, no τ_any, no copy bound, no pooled row, and no POST HOC block. The masked3 ledger rows that the frozen `score` writes beside every non-zs run never enter a row. Mutant B13 checks this.
- **The stored Qwen2.5-VL `zs`.** The stored stage-2 `zs` (5bf37a77 on OV-dev-B, d11b8f8a on XM-dev500) enters the `score` call only because `score_set` needs one `zs` per backbone (run doc §8, its `pcm_vs_zs` columns). No block-3 row reads it.
- **CC-368 N4(c), the identity row against the stored C-T1 decodes: NOT RUN, not coded.** The stored C-T1 `lmcap_ri` and `ret_img` runs have no pin in `STORED_SHA256` (block-3 run doc §12 O1). Opening them would also cross the custody line. N4(d) binds the paper: no C-T1 `lmcap_ri` level is ever mixed with a block-3 contrast.

## 5. Host commands, in order (from the repo at H_S; CPU only; `nice -n 19`; no GPU job on the host; `CUDA_VISIBLE_DEVICES=`)

`H_S` is the full 40-hex value of the scoring commit (CC-362 Q4). `C=/root/c_attr_checks_b3score; mkdir -p $C`. This folder lies outside `/root/outputs`, so the same path serves both options of §8 P8. Every `--prev` value is copied from the LOG line, never from the terminal.

**S0. Owed records of the scoring code.** None has run: the laptop runs no test (PI rule). Where they run is §8 P8.
```
for f in c_attr c_attr_lists c_attr_score; do /root/vsps/.venv/bin/python -I -B scripts/c_attr/$f.py --selftest; done > $C/selftest.log 2>&1
for v in venv-lb venv-t1; do /root/$v/bin/python -I -B scripts/c_attr/c_attr.py --selftest >> $C/selftest.log 2>&1; done
sha256sum $C/selftest.log > $C/selftest.log.sha256
/root/vsps/.venv/bin/python -I -B scripts/c_attr/c_attr_mutants.py --no-netns --jobs 4 > $C/mutants.log 2>&1; echo "rc $?" >> $C/mutants.log
sha256sum $C/mutants.log > $C/mutants.log.sha256
```
The expected values are exact. Any other count is a STOP, and the fix goes to the judge; nothing is patched on the host.

| check | expected |
|---|---|
| `grep -c '^selftest ok: ' $C/selftest.log` | 3 |
| `grep -c '^c_attr_lists selftest ok: ' $C/selftest.log` | 1 |
| `grep -c '^c_attr_score selftest ok: ' $C/selftest.log` | 1 |
| `grep -c 'selftest ok' $C/selftest.log` | 5 |
| `awk -F'; ' '/^selftest ok: /{print NF}' $C/selftest.log` | 22, 22, 22 (c_attr.py is unchanged since CC-368 H2) |
| `awk -F'; ' '/^c_attr_lists selftest ok: /{print NF}' $C/selftest.log` | 5 |
| `awk -F'; ' '/^c_attr_score selftest ok: /{print NF}' $C/selftest.log` | **22** (the 20 of record + 2 new items, none of which holds "; ") |
| `grep -c 'block 3 stages on a planted tree' $C/selftest.log` and `grep -c "block 3: the decoder's run ids" $C/selftest.log` | 1 and 1 |
| `$C/mutants.log` | exactly one line "control: the three self-tests pass on the unmutated files"; `grep -c ': KILLED'` = **107** (83 of record + B11–B34); `grep -c 'SURVIVED'` = 0; the line before `rc 0` is exactly "107/107 killed; survived: none" |

**S1. Staging (one OPS line; hashes only; no file opened).** The following go to the host, each checked against its pin on the laptop and on the host, with mode 444:
- `/root/c_attr_score_b3/in/stage2_ledger.jsonl` = the stage-2 ledger of record, `be716482c6f934e975bdbc58927cfc42a4c0ff589c9c5f95affd67c03eac0938`;
- `/root/c_attr_score_b3/in/c_attr_nomination.json` = `data/results/c_attr_1112_score/res/c_attr_nomination.json`, `559c18c1ba173cfbfed488d2bb7f7d797b66d681bd69aec51944f0c4e88ebdfa`;
- `$NCS_DATA/datasets/openviic/uit-openviic-annotation-dev.json` `550cfe06b06084976e81286531f7f4e52bea717e29004c699ccaf1e48919bdff` and `$NCS_DATA/datasets/c_xm_dev500/xm_dev500_data.json` `0da82355b65ab284fe55fc0d3c4101090301767347a02721890556618ca4905f`, from `.session_backup/2026-10-22/c_stage2/subsets/` exactly as CC-362 S1–S3 (no rebuild, never opened);
- under `/root/outputs/c_stage2/runs/`, the six stage-2 OV-dev-B runs of `c_attr.C2_RUNS` plus `c2_qwen25vl_7b_xm_dev500-zs.preds.json` (d11b8f8a), each at its `STORED_SHA256` pin;
- `$NCS_DATA/vncorenlp/VnCoreNLP-1.2.jar` `9e2811cd…`, with its `models/wordsegmenter/` files (their sha256 go into `VERIFY.json`), and a Java runtime.

Nothing else is staged, and no test file.

**S2. Verify.**
```
bash scripts/c_attr/c_attr_score_job.sh H_S b3verify --b3-sums B3SUMS
```
- **It writes:** `res/VERIFY.json` and `led/parity_c2.jsonl`.
- **It must show:**
  - `trees.b3.files` = the line count of the pulled `c_attr_b3/SHA256SUMS`;
  - `pins` with 5 entries;
  - `d1` equal to the cap line;
  - `parity_7_1.result` = ok.
- **OPS line:** the VERIFY sha256, `trees.b3.files`, `d1`, the `env.packages_sha256` value, `env.vncorenlp_models`. **STOP.**

**S3. K5 first.**
```
bash scripts/c_attr/c_attr_score_job.sh H_S b3k5 --prev <VERIFY sha>
```
- **It writes:** `res/K5.json`, `res/STAGE_b3k5.json` and `led/k5.jsonl`.
- **The K5 LOG line** gives the K5.json sha256, then the verdict, then the row:
  `<utc> OPS-<id>-c-b3-k5: K5 <DETECTED|NOT DETECTED|NOT RUN>; LMCap τ_sel OV-dev-B <d> [<lo>, <hi>], p <p>, label <label>, m = 1; K5.json <sha>; consequence: <K5_OUT text>`.
- It is written **before b3rest runs**. Until that line exists, nothing else of block 3 is read or computed. **STOP.**

**S4. The other rows.**
```
bash scripts/c_attr/c_attr_score_job.sh H_S b3rest --prev <K5 sha>
```
- **It writes:** `res/B3_SUMMARY.json`, `res/STAGE_b3rest.json`, `led/b3_ov_dev_b.jsonl` and `led/b3_xm_dev500.jsonl`.
- **OPS line:** the B3_SUMMARY sha256, the row keys per set, `not_run`. **STOP.**

**S5. Pull.**
- Pull `/root/c_attr_score_b3/{res,led,logs}` and `$C` to `.session_backup/machines/ATTR_H3/root/` (the host name of the block-3 pull, run doc §7). Check each logged sha256 and the folder digest, then make a 444 copy.
- The `in/` copies are not pulled again: the laptop holds their originals.
- The two reference files are then removed from the host, and the removal is logged (CC-362 N2).
- The host is then deleted after backup (PI-1109g), unless an approved next job is queued.
- Records commit (a later gatekeeper line, as CC-363): `res/` and `logs/` only. Never committed: `led/` (binding 6, CC-363 W6), `in/`, any `.preds.json`.

## 6. Stop rules and the K7 date rule

- **K7 is the only hard date** (v1.1 §10.1, CC-368 ruling 6): 2026-11-16 12:00 VN = 2026-11-16T05:00:00Z. A K5 verdict that is not written by then is **NOT RUN**: the CC-363 ruling 5 line ("the word 'test' … the positive control was not run") stands, and third-party rows are not interpreted.
  - The code refuses `b3verify`, `b3k5` and `b3rest` at and after that instant (`k7_open`, first in `cmd_stage`). So no verdict can be produced late.
  - A stage already running at 05:00Z is killed by the operator, and its file, if it exists, is not used.
  - Aim: the K5 LOG line by 2026-11-15T16:59Z (end of 11-15 VN). A verdict after that but before K7 stands as a logged schedule slip (CC-368 Q1 default).
- A `SCORE STOP`, a `REFUSED`, a parity failure or a non-zero rc stops scoring. Nothing is re-run with changed inputs, and the matter goes to the judge.
  - Proposed, binding only if the judge accepts §8 P14: the CC-348 judge line for environment-only failures of verify before `VERIFY.json` exists (jar, segmenter files, Java, an import) applies to `b3verify`. The operator removes `in/b3` and `led/parity_c2.jsonl`, repairs the environment without changing a pinned file, and runs `b3verify` once more, logging both attempts. Without that acceptance, such a failure goes to the judge.
- Every stage runs once. No byte under `scripts/c_attr/` changes between S0 and S5; the wrapper checks HEAD, the tree and SHA256SUMS at every call.
- `score`, `nominate`, `summary` and `copybound` are never called directly on a block-3 output, and `--work` is never passed on the host.
- No stage runs while any `/root/outputs/c_attr*/RUNNING` exists, or beside a GPU job.

## 7. Custody (what may be read during scoring)

- **May be read:**
  - the wrapper lines in `logs/score.log` and the last line of each stage log;
  - `$C` gate logs (counts);
  - `VERIFY.json` (the fields named in S2);
  - `K5.json`, once written;
  - `STAGE_*.json`;
  - `B3_SUMMARY.json`, but only after the K5 LOG line.
  These hold ids, labels, numbers and hashes only.
- **Not opened by the operator:**
  - `led/*.jsonl` (per-image ledgers; pulled 444 for a judge's recomputation, as in CC-363);
  - `in/` (caption copies);
  - any `.preds.json`, `.lists.json` or partial file;
  - the reference files (hash only);
  - the memory caption files;
  - the stored C-T1 decodes;
  - `~/vsps_labels/`, `~/.vsps_sealed`;
  - any test-set file.
- **Test sets.** No test set is staged, scored or opened. `b3verify` refuses any test-set file name in the output tree or among the pinned inputs, and the open() hook stays installed on h1.
- **Hosts.** No host name, IP or port appears in any repo file or LOG line.

## 8. Open points for the judge (each with my recommended reading)

- **P1 K7 in code, for all three stages, verify included.** Recommended: accept. It is the literal reading of "every unfinished step is NOT RUN". A late verify has no use, because K5 could not follow it. CC-368 N2 asked for a K7 guard in the decode job, and this adds one on the scoring side only.
- **P2 The order of K5 and the rest.**
  - `b3k5` scores only `lmcap_ri` and `lmcap_rand` on OV-dev-B. That `score` call also writes their masked3 rows, the frozen X2 behaviour of `c_attr.cmd_score`, and they are never used.
  - `b3rest` reads the K5 ledger back instead of scoring the two arms again, because `set_columns` refuses duplicate keys. It also checks the result against `K5.json`.
  - Recommended: accept as the meaning of "before any other block-3 row is computed or read".
- **P3 The stored stage-2 Qwen2.5-VL `zs` inside the `score` call.** CC-368 ruling 3(e) says stored decodes never enter a block-3 contrast. This one enters no contrast. It is a scorer requirement for the `ret_img` and `rand_img` ledger rows (run doc §8). Recommended: accept, and state it in the report.
- **P4 "Beside the text-only τ_sel" (§7.10).** Recommended: a file::key pointer to the batch-1 text τ_sel already read in CC-363, with no difference row. A difference would be an unregistered contrast between two decode policies on two hosts.
- **P5 N4(c) identity row.** Recommended: NOT RUN. The stored C-T1 decodes are unpinned and outside custody. The paper says so in one line.
- **P6 Tier strings (O8, §7.8).** As in §3–§4. Recommended: accept. The K5 row is a first look at the contrast, and its `lmcap_ri` level was seen. LMCap τ_pair and τ_marg do not carry the split words. XM-dev500 rows carry "no rule".
- **P7 The two NOT RUN paths.**
  - LMCap D1 not PASS: a NOT RUN K5 file is written, `b3rest` runs on the Qwen2.5-VL rows, and those rows are stamped uninterpreted.
  - A K5 arm missing beside a D1 PASS: refused, no file, nothing scored until a judge line.
  - Recommended: accept, as run doc §2 and §4 respectively.
- **P8 Where the owed records S0 run.** `/root/vsps` must stay at `60358b2`, clean, until the decode job ends. Two options:
  - (a) **Default:** after the decode ends and the pull is verified, check out H_S in `/root/vsps` and run S0. This costs the mutant wall time, which is not measured here: 107 mutants × 3 self-tests at `--jobs 4`, after K5's decodes.
  - (b) During decode call 2, a scratch clone `/root/vsps_s` at H_S, outside `/root/vsps`, `/root/outputs/c_attr*`, `/root/ncs-data` and `/dev/shm/c_attr_b3`. It would run S0 with the wrapper path replaced by `/root/vsps_s`, under the CC-368 ruling 8 guards and one DEVIATION line.

  Recommended: (b), named by the judge as a ruling-8 job, because it keeps the mutant time off the K7 path. Without that line, (a).
- **P9 Scoring environment on h1.** `/root/vsps/.venv` on the fresh host is not the HC2 environment (`env.packages_sha256` e95831b6 of the 1b VERIFY). Recommended: log the new importlib package-list sha256. The §7.1 parity gate is the binding check (CC-348, CC-363 1e). Equality with e95831b6 is not required.
- **P10 The nomination file `559c18c1…`** is staged only because `score` refuses any OV-dev-B `at_` run without a v1.2 nomination file (V4 (1), SC1). No block-3 row uses it. Recommended: accept, and pin it, as coded.
- **P11 Test-set names.** The rule is 'test' between separators or digits, or a registered test-set key (`c_attr.TEST_SETS`). Its ceiling: it checks names, not contents. The readers' id checks (`references2`), the open() hook and the custody rules stay in force. Recommended: accept.
- **P12 STEP3 against the cap line.** The code records `d1` only. The comparison with the cap line is an operator gate before S2 (§2). Recommended: accept. A code check would need the logged values as arguments.
- **P14 The CC-348 environment-failure line, carried over to `b3verify` (§6).** It was ruled for the 1b verify. Recommended: accept, for environment-only failures before `VERIFY.json` exists. `b3verify` scores nothing, and the §7.1 parity gate re-runs on the repaired environment.
- **P13 N5.** The block-3 run doc l.9 diff base reads `d10874e`, and it is byte-equal at `f267815` (CC-368). This package's diff is against `60358b2`, where `scripts/c_attr` holds the committed decode code. Nothing else is owed.
