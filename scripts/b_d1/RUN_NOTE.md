# RUN NOTE v2: B-D1/A3 code (Paper B), after the S0 code read CC-506

Written 2026-11-27 by agent b-d1. The registration is `manuscript/prereg/2026-11-27_b_d1/PREREG_DRAFT_B_D1_A3_v3.md`: sha256 `bf3a55f7…`, commit `adebac7`, rulings CC-505 and CC-505r2.

## v2 after CC-506 (CONDITIONAL GO 87)

- **W1 and W2.** `b_d1.py` is the judge's file, byte for byte (`4e044401`):
  - **W2:** G0 adds `sig_mismatch`, the number of F_dev classes whose sig differs from `DEV.json`. Any mismatch is a FAULT. A difference within 1e-6 could still move L or U across 0; the gate makes every sig-dependent result on the matrix equal to the one taken from `DEV.json`.
  - **W1:** the A3 maximum per-member rate is taken over the 54 F_dev members (§5 A3), in the key `max_member_rate_F_dev_DESCRIPTIVE`.
- **W3.** `host_selftest.sh` is the judge's file, byte for byte (`602626b5`):
  - the summary greps work for any count;
  - the S0 `.time` record is copied into the outputs;
  - each wheel of `WHEELS_SHA256.txt` is downloaded at its own version with `--no-deps --only-binary=:all:`;
  - every listed wheel is required.
- **W4.** `test_b_d1.py` has 41 checks (v1: 34). `mutants_b_d1.py` has 84 mutants: the 38 v1 triples verbatim, plus the 46 judge pairs of `JUDGE_MUTANTS_CC506.py` verbatim, each with a named check.
  - New checks: `fe_claims`, `h1_h2_tests_and_holm` (pooling, the four exact p-values, Holm at 0.05, the H1 and H2 comparators at their K, and per-member against per-class AER), `h1_h2_fixture_k`, `h2_descriptive_rows`, `g0_verdict_over_F`, `g0_sig_gate` (L crosses 0 by under 1e-6) and `a3_counts_by_family`.
  - Extended checks: `fold_construction` (H_u holds all 18 members), `held_break_and_discordant` (breaks judged on H_u), `stage_guards` (s2 refuses a G0 that passed on another matrix), `identity_m1_m1prime` (the identity over the G passed) and `a3_rule_on_f0` (a member-keyed fixture; a uts member with the largest rate is excluded from the maximum).
  - `check_cc506.py` prints `CC506 CHECK PASS`. The output is in `CHECK_CC506.txt`.
- **W5.** `SHA256SUMS` lists the v2 files. The host S0 record (ruling 5, below) is pinned on the LOG before any data push.

**K6 holds.** No D1 or A3 quantity has been computed on any data.

**Laptop debug run** (laptop exception OPS-1127x, 2026-11-27; synthetic fixtures only; `python3 -X utf8 -I -B` in a scratch venv with numpy 2.5.4 and scipy 1.18.1, on an ext4 scratch copy of the tree; `NCS_DATA` set to an empty directory; no data-set file and no study output read).
- v1: 34 ok of 34; killed 38 of 38.
- v2: `test_b_d1.py` gives **41 ok of 41 checks**; `mutants_b_d1.py --jobs 4` gives **killed 84 of 84**, each by its named check printing FAIL; `check_cc506.py` gives **CC506 CHECK PASS**.
- The logs are in `LAPTOP_DEBUG_RUN.txt` and `CHECK_CC506.txt`.
- **The record of authority is the host re-run through `host_selftest.sh`** (PI-1111). The env toy check (`--env`) was not run on the laptop: it needs the pinned Java and segmenters.

## Files

They belong in `scripts/b_d1/` of the vsps tree; shas are in `SHA256SUMS`.

| file | role |
|---|---|
| `b_d1.py` | stages `s1` (re-score), `g0` (reproduction gate), `s2` (H1, H2, H3, A3), `budget` |
| `test_b_d1.py` | 41 self-tests on synthetic fixtures; marker syllable `zqxv` |
| `mutants_b_d1.py` | 84 mutants of `b_d1.py` (38 own, 46 from CC-506), each killed only by its named check printing FAIL |
| `run_tests.sh` | runs the self-tests and the mutants, plus the toy environment check with `--env` |
| `run_stage.sh` | runs one stage under the 8 CPU-h hard stop |
| `host_selftest.sh` | sets up a fresh rented host and runs S0 |
| `LAPTOP_DEBUG_RUN.txt`, `CHECK_CC506.txt` | the laptop debug-run logs (OPS-1127x) and the CC-506 closure check |
| `WHEELS_SHA256.txt` | the pinned wheel list of the FE-CERT host (byte copy of `.session_backup/machines/ATTR_H1_misc/outputs_bfe_checks/wheels_sha256.txt`, `51cc8778…`) |

## Reuse and pins

`b_fecert.py` (`67e43dea…`) is imported unchanged, together with every repository file it loads: 24 modules plus `tools/obj_rater/pair.html`, listed in `b_d1.PINS` with their sha256.
- `pin_check()` runs before the import. Any file missing or off its pin stops the run with a FAULT.
- `closure_check()` runs after the import. A repository module that was loaded but is not in PINS stops the run with a FAULT.

The FE-CERT functions used:
- `env_record`, `env_check` (pinned environment, r* included, exactly as in FE-CERT);
- `ktvic_texts` (every output file checked against `SYSTEMS.tsv` by sha256);
- `scorer` (the matched member on outputs and references; document frequencies from the references);
- `boot_W` (seed 20261112, B = 10,000);
- `stats`, `sig`, `zval`, `certify`, `held_break`, `holm`, `cp_lower`, `cp_upper`, `N_MIN`, `R_MAX`, `F0N`.

The family comes from `family.py`.

## Stages (prereg v3 §6)

| stage | reads | writes | gate |
|---|---|---|---|
| s0 | the tree | records only | all 41 checks ok, 84 of 84 mutants killed, `ENV OK` (`env_check` and F3 on the toy strings) |
| s1 | `FAMILY.json` `431d92a4`, `CENSUS.json` `2252167b`, `SYSTEMS.tsv` `30ac9555`, `test_data.json` `cc22ec6a`, the 73 own files and the 2 baselines | `PER_IMAGE_D1.npz` (CIDEr-D per member × file × image, token-identity hashes, member and file names; mode 444; never committed) and `S1.json` | registration sha; `env_check`; 75 files on 558 images; units as in FE-CERT (none dropped, `uts` held out) |
| g0 | `DEV.json` `88ff39aa`, `RESULT.json` `25614b46`, the npz by `--npz-sha` | `G0.json` (counts and differences only) | (a) on F_dev classes: same key set, same sorted members, every \|Δ\| ≤ 1e-6 on D, L, U, sd, and the same sig as in `DEV.json` (W2). (b) the verdict over F (72) equals `RESULT.json` `F`, and D_f0 equals the stored value within 1e-6. Fail → rc 3, FAULT, stop |
| s2 | `DEV.json`, the npz, `G0.json` by `--g0-sha` | `RESULT_D1.json` (counts, rates, nominal p-values, bounds, labels; no per-comparison rows) | refuses unless G0 passed on the same npz sha |

Each output is written once and set to mode 444. A second run refuses.

The order on the host is s0, s1, g0, s2. Between stages the coordinator pins the sha256 of each output on the LOG before passing it to the next stage. Nothing from s2 is opened before its pin line.

## Coded readings (for the judge)

1. **Class building.**
   - Classes are built from the matrix in F_ALL order: the 54 F_dev members first, then the 18 `uts` members. A class that mixes both is built as in FE-CERT stage 2b.
   - The class key is `key(a)|key(b)|key(refs)`, as in `b_fecert.add_class`.
2. **G0.**
   - G0 compares CIDEr-D only, because the matrix holds only CIDEr-D. H3 reads BLEU-4 and ROUGE-L from the stored `DEV.json`.
   - `RESULT.json` is filtered to `set == "D"`.
   - These stages run with `OMP_NUM_THREADS=2`. The FE-CERT stages ran with the default thread count (`b_records/1.args`, `2b.args`); only its self-test runs set 2. BLAS threading can move a statistic by about 1e-13, far inside the 1e-6 tolerance.
3. **M1′ (union-of-ties).** Each member of G is one contract. A member counts as tied when its class's CI contains or touches 0. When every contract is significant but in mixed directions, no ordering is claimed. M1′ must equal `certify` on every D comparison over F_dev, or the run stops with a FAULT.
4. **M3 and M4.** The candidates have `sig_f0 ≠ 0`. The direction is `sign(D_f0)` and the margin is `zval` of the f0 class.
5. **M2 (AER).**
   - σ_c is the SD (ddof 1) over all 75 files of the corpus CIDEr-D under member c. It is computed once and held fixed. A σ_c ≤ 1e-9 is a FAULT.
   - The ensemble is `e_i = mean_c d_{i,c} / σ_c`, with equal weight per member and statistics from `BF.stats` with the shared W.
   - The per-class reading (the mean within each class, then the mean over classes) is DESCRIPTIVE.
6. **Size matching.**
   - K = min of the two native sizes.
   - Each method keeps its top K by its own margin: z_min for M1, z_f0 for M3, z_E for M2.
   - Ties are broken by comparison id ascending, for every method.
7. **Discordance.** A claim is (id, direction). A claim with the same id but the opposite direction counts on both sides. A break is `held_break` under H_u, unchanged.
8. **Tests.**
   - p = `binomtest(k, n, 0.5, "greater")`, exact and one-sided; n = 0 gives p = 1.
   - All four p-values always enter `BF.holm` at 0.05. Holm's reject flags are reported, not adjusted p-values.
   - Label order: n < 10 gives NOT_EVALUABLE; then SUPPORTED; then `<X> BETTER`; otherwise NOT SUPPORTED.
9. **H3.**
   - A contract is a (metric, member) pair. A grid is certified when every contract is significant in the same direction.
   - n counts certificates over G_contract (18 `tw` members × 3 scorers). k_T counts those not certified over G_caption (54 × 3).
   - The label uses `BF.cp_lower` and `BF.cp_upper` (one-sided 95%) against `R_MAX` = 0.05, with `N_MIN` = 59.
   - The split is the number of k_T comparisons with a breaking added class per unit.
   - k_U and k_TU come from the `syl` `tw` grid and are DESCRIPTIVE.
10. **A3.**
    - The draws are `default_rng(20261127).choice(1101, 1000, replace=False)` over the order of `DEV.json`. Draw j uses the swap vector `default_rng(20261127 + j).integers(0, 2, 558) * 2 - 1`, applied to every member.
    - j counts from 0, so draw 0's swap seed equals the seed of the pick. The registered wording ("seed 20261127 + index") allows this.
    - The classes are those of the real comparison.
    - The label follows the rule on r_f0, per direction: one-sided 97.5% Clopper–Pearson from `scipy.stats.beta`, pass at upper ≤ 0.040, ABOVE at lower > 0.025.
    - r_A3 over F_dev and over F, and the maximum per-member rate over the 54 F_dev members (W1), are printed beside it.
    - Draw 0's swap seed equals the pick seed (20261127). The result note carries this fact.
11. **The 8 CPU-h hard stop** (`run_stage.sh` with `b_d1.py budget`).
    - Before a stage: seconds left = 28,800 minus the user+sys of every `*.time` record. The stage is refused when that is 0 or a STOP marker exists.
    - During the stage: GNU `time -v` and `prlimit --cpu=<seconds left>`. The Java segmenter is a child process with its own limit, so the cumulative check after the stage is the binding one.
    - Outputs go to a staging directory and are moved into place only when rc = 0 and seconds remain. Otherwise STOP is written, nothing is kept, and a judge line is needed.
    - S0 counts toward the budget too.
    - **As measured by the judge (CC-506 C6):**
      - no result produced past 8 CPU-h is kept;
      - CPU itself can overrun by up to one child process's run, because each child has its own `RLIMIT_CPU`;
      - the cumulative check after the stage then writes STOP.
    - Only the coordinator removes STOP, after a judge line on the LOG. `*.time` records are never deleted, so the budget stays cumulative over every run.
    - Tool prechecks run outside the budget, in `host_selftest.sh` step 0: GNU `time`, `prlimit` and the VnCoreNLP models. The install bundle lists `time` and `util-linux` (`scripts/host_bundle/SYSTEM_PACKAGES.txt` l.22, l.24). A missing tool therefore fails before S0 and never writes STOP.

## Host run (rented host only; after the C-CONF floor is paid, CC-505 ruling 9)

1. **Push and set up.** Push the tree to `/root/b_d1_tree`. It holds the PINS files, the registration file and `scripts/b_d1/*`. Build it on the laptop from the repository root, with `$H` the host alias (never written to a file):
   ```bash
   tar -cf /tmp/b_d1_tree.tar $(python3 -c "s=open('scripts/b_d1/b_d1.py').read(); b=s[s.index('PINS = {'):s.index('}\n', s.index('PINS = {'))]; print(' '.join(l.split('\"')[1] for l in b.splitlines()[1:] if l.strip().startswith('\"')))") \
     manuscript/prereg/2026-11-27_b_d1/PREREG_DRAFT_B_D1_A3_v3.md scripts/b_d1/{b_d1.py,test_b_d1.py,mutants_b_d1.py,run_tests.sh,run_stage.sh,host_selftest.sh,WHEELS_SHA256.txt,RUN_NOTE.md,LAPTOP_DEBUG_RUN.txt,CHECK_CC506.txt,SHA256SUMS}
   ssh -o BatchMode=yes $H 'mkdir -p /root/b_d1_tree && tar -xf - -C /root/b_d1_tree' < /tmp/b_d1_tree.tar
   ```
   Then: After the install bundle (PI-1115r), the jar and models go to `/root/ncs-data/vncorenlp`. Then run:
   `bash /root/b_d1_tree/scripts/b_d1/host_selftest.sh`. It checks the tree sha, Python 3.12.3, Java 21.0.13.0.3, the jar `9e2811cd`, the wheels against `WHEELS_SHA256.txt`, and S0 under `run_stage.sh`.
   **The S0 record (CC-506 ruling 5).** The coordinator pulls and pins it on the LOG before any data push; S1 starts only after that pin. It consists of:
   - `/root/outputs_b_d1_checks/`, holding:
     - `host_selftest.log` with `HOST_SELFTEST PASS`;
     - `s0.log` with `selftest: 41 ok of 41 checks`, `killed 84 of 84` and `ENV OK` with its env and F3_equal JSON line. Compare F3_equal with `FAMILY.json::F3` (N3);
     - `b_d1_sha_check.txt`, all OK;
     - `java_version.txt` (21.0.13.0.3), `jar_sha256.txt` (9e2811cd);
     - `wheels_sha256.txt` (34 lines, each in `WHEELS_SHA256.txt`), `pip_freeze.txt`;
     - the `s0.<utc>.time` record;
   - `/root/outputs_b_d1_checks.sha256`, written outside the directory and pulled separately. It must pass `sha256sum -c` on the pulled copy;
   - the listing of `/root/b_d1_records/`, with no STOP.
2. **Push the data.** Push the work files (`FAMILY.json`, `CENSUS.json`, `SYSTEMS.tsv`, `DEV.json`, `RESULT.json`), `test_data.json`, the 73 own files and the 2 baselines. Check their shas on both sides.
3. **Run the stages** with `PY=/root/venv-bd1/bin/python` and `NCS_DATA=/root/ncs-data`, from `/root/b_d1_tree`:
   - `bash scripts/b_d1/run_stage.sh s1 /root/b_d1_records /root/b_work /root/b_d1_out --baselines /root/b_baselines --pyvi-wheel /root/bd1-wheels/pyvi-0.1.1-py2.py3-none-any.whl --uts-wheel /root/bd1-wheels/underthesea-9.5.0-py3-none-any.whl` → pin `PER_IMAGE_D1.npz` and `S1.json` on the LOG;
   - `bash scripts/b_d1/run_stage.sh g0 /root/b_d1_records /root/b_work /root/b_d1_out --npz-sha <npz>` → pin `G0.json`. If rc 3: stop and write a judge line;
   - `bash scripts/b_d1/run_stage.sh s2 /root/b_d1_records /root/b_work /root/b_d1_out --npz-sha <npz> --g0-sha <G0>` → pin `RESULT_D1.json`.
4. **Pull and clean up.** Pull the records and the outputs (the npz stays uncommitted). Delete the host, then clean it per PI-1115s.

CPU: about 4.5 CPU-h expected, with the hard stop at 8 (COMPUTE_B_D1_v2.md).
