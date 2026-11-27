# RUN NOTE v3: B-ALT FE-LOCUS code (Paper B), round 3 (the last) after CC-512r2

Written 2026-11-27 by agent b-alt.

**Base.** v3 starts from v2, `~/vsps_ro3/b_alt_code_v2` (SHA256SUMS `2cfdf0e7`). The diff is `V2_TO_R3.diff`.

**What I did not use.** An r2 folder, `~/vsps_out/b_alt_code_r2`, crossed with CC-512r2. Its coded H5 window, its `host_checks.sh` and its own `host_selftest.sh` are **not** carried into v3. Ruling 2 makes H2's tar sha and H5–H7 coordinator record checks. Only its new self-tests are carried over.

## v3 after CC-512r2

| item | what v3 does |
|---|---|
| W2b | `host_selftest.sh` is byte-equal to `expected_fixes/host_selftest.sh`, `37578da0…`. `BALT_BASE` is required and has no `/root` default |
| W3 | `test_b_alt.py` now has 48 checks (14 new). They compare against literal registered values, among other checks. On the v3 tree built by `make_tree.sh`, `JUDGE_MUTANTS_CC512r2.py` (`06270758…`) gives **KILLED 38 of 38**, with J22 killed by FAIL. The log is `JUDGE_MUTANTS_CC512r2_v3.log`. The package's own mutants: killed 60 of 60. Self-tests: 48 ok of 48 |
| W3: J35 | `changed_needs_significance_under_f0` stubs `certify` to report a certificate on a world where every difference is 0. The count of CHANGED must then stay 0. So the `s0 != 0` term of the CHANGED line is tested directly, not only through `certify` |
| b_alt.py | Byte-equal to v2 (`7dc734c8`). No mutant exposed a bug in a verdict line, so no verdict line was changed |
| W2c | §Host below gives the command and the record file for each of H1–H7 on host (b) |
| W4 | On a guard kill, the GNU `time` record can under-count the tree's CPU (CC-512 C5). STOP is terminal, so nothing depends on it |
| W5 | `syl_key` computes NFC, then the tm rule, then casefold. §3.2 lists "NFC, lower case, tm". The two orders commute for the tm rule (CC-512 C4, J2 killed) |
| W8 | Not done (optional). The `--env` toy check still runs through the stdin here-doc of `run_tests.sh`, which works as CC-512 C6 and CC-512r2 D4 show |

**Coded reading 6, disclosed (CC-512 ruling 3).** c_ref^B and c_out^B are tallied in s1b, after `CENSUS_ALT.json` is pinned, and s2 recomputes them in every draw. "Counted at S2" in §3.4 is met as a timing label.

**Not registered, disclosed if it fires (CC-512 ruling 4).** A zero denominator in any bootstrap draw gives NOT_EVALUABLE.

**Registration.** `manuscript/prereg/2026-11-27_b_alt/PREREG_DRAFT_B_ALT_v2.md`, sha256 `ed05acdb7682b516738b00d2741fd87d0220e30eec9aa38ae5a2a92c3014f352` after the alias redaction (CC-510e1, commit `2d3c39f`; it was `eddade6d` at `74e5034`). Erratum `ERRATUM_B_ALT_1.md`, sha256 `8367faceffbd2235d2c4cfe2a0b768c37e0e1d357140a995db5359c9a884958f` (CC-510e2, commit `7f7cf4f`), replaces the §5 host rule. Rulings CC-510 and CC-510r2, PI-1127k. `reg_check()` pins both files in full.

**No FE-LOCUS quantity has been computed on any data.** The laptop runs below used invented fixtures only:
- `NCS_DATA` pointed to an empty directory;
- no data-set file, system output or study output was read;
- nothing was written to `/mnt/d`. The repository was read with `git archive` only.

## Files

These belong in `scripts/b_alt/` of the vsps tree. Their sha256 values are in `SHA256SUMS`.

| file | role |
|---|---|
| `b_alt.py` | stages `s1a` (census on half A), `s1b` (re-score plus image-level disagreement counts), `g0` (reproduction gate) and `s2` (estimands, floors, labels, DESCRIPTIVE rows) |
| `cpu_guard.py` | CPU guard over the whole process tree (stdlib only) |
| `test_b_alt.py` | 48 self-tests on invented fixtures. The marker syllable is `zqxv`; the invented syllables are `zba`, `zbe`, … and `ghoà` / `ghòa` |
| `mutants_b_alt.py` | 60 mutants, each killed only by its named check printing FAIL |
| `run_tests.sh` | runs the self-tests and the mutants; with `--env`, also the toy environment record |
| `run_stage.sh` | runs one stage under this study's own 8 CPU-h stop |
| `host_selftest.sh` | the judge's file, `37578da0`: sets up host (b) inside `BALT_BASE` and runs S0 |
| `make_tree.sh` | builds the push tree from `PUSH_LIST.txt` only, on ext4, and runs the closure check |
| `PUSH_LIST.txt` | the push list: 41 repository-relative paths |
| `WHEELS_SHA256.txt` | byte copy of `scripts/b_d1/WHEELS_SHA256.txt` (`51cc8778…`) |
| `LAPTOP_DEBUG_RUN.txt` | logs of the laptop debug run |

## Reuse and pins (unchanged code)

**FE-CERT, imported unchanged.**
- `b_fecert.py` (`67e43dea…`) is imported together with every repository file it loads. These are the same 24 modules plus `pair.html` that `b_d1.PINS` pins at `38067d1`.
- `pin_check()` runs before the import, and `closure_check()` runs after it.
- The closure check ignores a `__main__` with no file behind it, such as a here-doc's `<stdin>`.

**`scripts/b_d1/b_d1.py`** (`4e044401…`, commit `38067d1`) is pinned and reused unchanged, for one thing only: `run_stage.sh` calls `b_d1.py budget --records <this study's records dir>`.
- `b_alt.py` does not import it. If it did, b_d1's own closure check would flag `scripts/b_alt` at import.

**FE-CERT functions used:**
- `env_record`, `env_check`;
- `ktvic_texts` (outputs checked against `SYSTEMS.tsv` by sha256);
- `boot_W`, `stats`, `sig`, `certify`, `F0N`, `REFS`, `Fault`, `B`.

**Family functions used:** `Tok`, `tone`, `key`, `members`, `F0`, and the level tuples, all from `family.py`.

**Changed relative to FE-CERT: `per_cider`.**
- It is `b_fecert.scorer` restricted to CIDEr-D and the token keys. It makes the same calls: `Tok.side("matched")`, `E4.Cider` with document frequencies from the references of all ids, and `FM.key`.
- The self-test `s1b_matches_fecert_scorer` shows equality with `BF.scorer` to 1e-12, keys included.
- G0 checks it against `DEV.json` on the real data.

**The jar is pinned in full (N8).** `env_ok` adds `jar_sha256 == 9e2811cdbc2ddfc71d04be5dc36e185c88dcd1ad4d5d69e4ff2e1369dccf7793` to FE-CERT's 8-hex prefix check. `host_selftest.sh` checks the full value too.

## Closure check (the push tree only)

`bash scripts/b_alt/make_tree.sh <repo> <code dir> <ext4 dest> <python>` does the following:
1. Takes the 26 pinned files at `38067d1`, and the registration and erratum 1 at `7f7cf4f`, by `git archive`. Then copies the `scripts/b_alt` files.
2. Refuses a missing or an extra file against `PUSH_LIST.txt`.
3. Checks the registration's sha256 and the erratum's.
4. Runs `python -I -B` inside the tree, with an empty `NCS_DATA`, importing `b_alt`, `cpu_guard` and `test_b_alt`. Their own pin and closure checks run at import. It then asserts that every loaded tree module is in the push list, and that no `__pycache__` or `.pyc` was written.

Laptop result: `imported 27 tree modules, all in the push list` and `CLOSURE PASS` (`LAPTOP_DEBUG_RUN.txt`).

**Push list** (`PUSH_LIST.txt`):
- the 26 PINS files of `b_alt.PINS`: the 25 of `b_d1.PINS`, plus `scripts/b_d1/b_d1.py`;
- `manuscript/prereg/2026-11-27_b_alt/PREREG_DRAFT_B_ALT_v2.md` and `ERRATUM_B_ALT_1.md`;
- the 13 `scripts/b_alt/` files.

## Stages (registered order, prereg v2 §5)

| stage | reads | writes | gate |
|---|---|---|---|
| s0 | the tree | records only | 48 of 48 checks, 60 of 60 mutants killed, `ENV OK` |
| s1a | `FAMILY.json` `431d92a4`, `CENSUS.json` `2252167b`, `test_data.json` `cc22ec6a`; **half-A references only** | `CENSUS_ALT.json`: counts, floor, Π_head and the dictionary as word-type keys. Host only; committed only if OQ4 is answered yes | registration sha, `env_ok`, 558 images. Floor (ii) is unaligned > 0.5%; floor (iii) is fewer than 30 types. A tripped floor is recorded, rc 0, and the chain stops at s1b |
| s1b | the census by `--census-sha`, `SYSTEMS.tsv` `30ac9555`, the 73 own files and the 2 baselines | `PER_IMAGE_ALT.npz`: CIDEr-D for 108 members × 75 files × 558 images, keys, and the image-level counts `[n_head, n_all, n_other, unaligned]` on references and on outputs. Plus `S1B.json` | refuses a census that tripped a floor; 75 files |
| g0 | `DEV.json` `88ff39aa`, the npz by `--npz-sha` | `G0_ALT.json` | over the 36 G_w members on all 558 images with the FE-CERT draws: same class keys, same members, every \|Δ\| ≤ 1e-6 on D, L, U and sd, the same sig, and 1,101 comparisons. Failure gives rc 3 |
| s2 | the census, the npz, and `G0_ALT.json` by `--g0-sha` | `RESULT_ALT.json`: aggregates and labels only | refuses unless G0 passed on the same npz |

Between stages, the coordinator pins each output's sha256 on the LOG before passing it on. Every output is written once and set to mode 444.

## Coded readings (for the judge)

1. **Split** (§3.2 step 0, N4).
   - Half B is kept in the registered list order `perm[279:]`. W_B rows index images in that order.
   - W_B = `boot_W(279, 20261128)`, with B = 10,000.
2. **Syllables and alignment.**
   - A token is split at `_`. A key is NFC of `tone(·, "tm")`, then casefolded.
   - A string is unaligned when a token has an empty piece around `_`, or when the two census members' key sequences differ.
   - Punctuation tokens are syllables with their own key.
3. **Spans.** These are the runs between consecutive common boundaries (shared token boundaries and the string ends) that have at least 2 syllables and in which the internal boundary vectors differ. The type is the key tuple.
4. **Ranking and dictionary.**
   - Types are ranked by count (descending), then by the code-point order of the space-joined type.
   - Π_head is the shortest prefix with `cum × 5 ≥ 4 × total`. Exactly 0.80 is included.
   - The dictionary pattern is the modal `rdr` pattern. A tie goes to fewer tokens, then to the smallest 0/1 vector.
5. **Pin** (§3.3).
   - The pin runs after the member's own steps, so after case, P-post and NFC; it moves boundaries only.
   - Matching is longest first, scanning left to right, from length `max |type|` down to 2.
   - Both ends of a match are forced to be boundaries.
   - A pinned member is `(U, T, P, C, tag)`, where tag `h` = Π_head and tag `a` = Π_all. It is applied through `Tok.side` to outputs and references alike, so document frequencies follow the pinned references.
   - "Unaligned under m" in §3.3 is read as a malformed token, with the string left unchanged. The count goes to `S1B.json::malformed_pinned_strings`. A single member has no second segmentation to compare against.
6. **c_ref^B and c_out^B.**
   - The image-level counts are tallied in s1b, after `CENSUS_ALT.json` is pinned, because tallying needs the segmenters. s2 reads them.
   - c_out sums over the 75 files per image.
   - Both are recomputed in each draw as `W_B @ n_head / W_B @ n_all` (mutant M10).
7. **Estimands.**
   - σ is fixed: the sign of the half-B mean raw shift per unit (c, ℓ).
   - The sums are linear, so each draw is `W_B @ vector / 279` (mutant M4).
   - κ_head = (A − A_h) / (A − A_a). Δ_lo and Δ_hi are computed per draw. [L, U] are the 2.5th and 97.5th percentiles.
8. **Floors.**
   - (iv) is checked, then (v).
   - A zero denominator in any draw also gives NOT_EVALUABLE.
   - A tripped floor replaces both labels, H-L1 and H-L2, with the floor string. The registration lists the floors before both hypotheses.
9. **DESCRIPTIVE rows:**
   - ρ_all split by T group (`tw` pairs against `tm`/`tf` pairs);
   - output-only occurrences;
   - unaligned strings;
   - how far the pin moves the reference member (Σ|D_r^Π − D_r| / Σ|D_r|);
   - floor sums;
   - FRAGILE and CHANGED over G_w, raw against Π_head-pinned, on half B with W_B.
10. **The 8 CPU-h hard stop, child processes included.** `run_stage.sh` uses three layers:
    - `b_d1.py budget` on `$BALT_BASE/b_alt_records`. It refuses a records path containing `b_d1_records`, so this study's budget is separate from D1's.
    - GNU `time -v` and `prlimit --cpu`, as in D1.
    - `cpu_guard.py`, which reads utime + stime + cutime + cstime of the stage and all its live descendants from `/proc` every 2 s, and kills the process group at the seconds left (rc 7, then STOP).
    - This closes the D1 gap (CC-506 C6) in which each Java child had its own RLIMIT_CPU.
    - The self-test kills a burning child, a burning grandchild, and a chain of reaped short grandchildren.
    - Overrun is at most 2 s × cores.

## Laptop debug run, v3 (synthetic only; this round used about 21 laptop CPU-min, within the 30 CPU-min allowance)

Python 3.12.3, numpy 2.5.4, scipy 1.18.1 (scratch venv). The tree was an ext4 copy built by `make_tree.sh`, with files at mode 444.
- Closure: **CLOSURE PASS** (27 tree modules). The PI-PC alias occurs 0 times.
- `test_b_alt.py`: **48 ok of 48 checks**.
- `run_tests.sh` (`JOBS=4`): **killed 60 of 60**.
- `JUDGE_MUTANTS_CC512r2.py <v3 tree> <python>`: **KILLED 38 of 38** (`JUDGE_MUTANTS_CC512r2_v3.log`).
- No `__pycache__` was written.
- The `--env` toy check needs the pinned Java and segmenters, so it runs on the host only.
- **The record of authority is the host run through `host_selftest.sh`.**

## Host run: host (b), the PI's PC, the only host (ERRATUM_B_ALT_1, CC-510e2; CC-512 ruling 6, CC-512r2 ruling 2)

`$B` = `BALT_BASE` is the one own folder (H1). `host_selftest.sh` refuses to run without it.

Its layout is the one `host_selftest.sh` uses:
- `$B/b_alt_tree`;
- `$B/ncs-data`, which holds `datasets/ktvic/test_data.json`, `results/` and `vncorenlp/`;
- `$B/b_baselines` and `$B/b_work`;
- `$B/venv-bd1` and `$B/bd1-wheels`;
- `$B/b_alt_records`, `$B/b_alt_out` and `$B/outputs_b_alt_checks`.

**Host preconditions** (`host_selftest.sh` fails closed without them): `PY3` set to a CPython 3.12.3 interpreter inside `$B` (CC-512e1; for example python-build-standalone 3.12.3 unpacked into `$B`, as D1 did; the host's system python is never used or changed), `java` on `PATH` reporting 21.0.13.0.3, GNU `time`, `prlimit`. The S0 record carries `interpreter.txt` (path, sha256, `sys.version`) and `java_path.txt` (path, sha256).

**Record checks.** Each record is written to the session record before the step it guards (E1). The coordinator runs them. The commands below run on the host unless they say laptop.

| check | when | command | record |
|---|---|---|---|
| H1 own folder | before the push | `mkdir "$B"` (a new folder in the agent's own work area); `ls -la "$B"` | `H1_<utc>.txt`: the path and the empty listing |
| H2 tar | laptop, before the push | `tar -C <ext4 staging> --owner=0 --group=0 --numeric-owner -cf ~/b_alt_push.tar b_alt_tree ncs-data b_baselines b_work`, then `sha256sum ~/b_alt_push.tar`. The staging folder holds the `make_tree.sh` tree and the data files, each checked by sha256: `test_data.json` `cc22ec6a`, `DEV.json` `88ff39aa`, `FAMILY.json` `431d92a4`, `CENSUS.json` `2252167b`, `SYSTEMS.tsv` `30ac9555` with the 75 output files checked against it, and the jar `9e2811cd…7793` | `H2_laptop_<utc>.txt`: the tar sha |
| H2 tar | host, after copy, before untar | `sha256sum "$B/b_alt_push.tar"` (must equal the laptop line); `tar -C "$B" -xf "$B/b_alt_push.tar"`; `find "$B" -name .git` (must be empty) | `H2_host_<utc>.txt` |
| H3 env and S0 | after H2 | `BALT_BASE=$B bash $B/b_alt_tree/scripts/b_alt/host_selftest.sh` (`env_check`, the full jar sha, the wheels, S0 under `run_stage.sh`) | `$B/outputs_b_alt_checks/` and `$B/outputs_b_alt_checks.sha256`, pulled and pinned on the LOG before any stage |
| H4 CPU stop | every stage | `run_stage.sh` (process-tree stop in `cpu_guard.py`; `prlimit --cpu` ≤ 28,800 as the backstop) | `$B/b_alt_records/<stage>.<utc>.time` |
| H5 C-CONF window | before every stage | `date -u; pgrep -af 'b_alt/cpu_guard.py'` | `H5_<stage>_<utc>.txt` |
| H6 pull | after s2 | host: `cd "$B/b_alt_out" && sha256sum RESULT_ALT.json PER_IMAGE_ALT.npz`. Laptop: pull to the home file system (never `/mnt/d`), then `sha256sum -c`, `chmod 444`, and pin on the LOG | `H6_<utc>.txt`: both sha lines |
| H7 wipe | after H6 | `rm -rf -- "$B"; ls -d -- "$B"` (must report it absent) | `H7_<utc>.txt` |

**H5 refusal rule (coordinator).** Do not start a stage if any of these holds:
- an FE-LOCUS wrapper is running;
- now + the stage's worst-case wall time crosses **2026-11-28T04:00Z**.
  - This is the C-CONF set-up time of CC-481r3 X-1. It is stricter than the erratum's 09:00Z, which CC-512r2 W2c quotes.
  - The rule holds until the LOG carries the C-CONF end line or the C-CONF chair's release.

**Worst-case wall bounds, fixed before S0:**

| stage | bound | latest start for 04:00Z |
|---|---|---|
| s0 | 1 h | 03:00Z |
| s1a | 1 h | 03:00Z |
| s1b | 8 h (the CPU stop) | 2026-11-27T20:00Z |
| g0 | 1 h | 03:00Z |
| s2 | 2 h | 02:00Z |

**Stages.** Run from `$B/b_alt_tree`, with `export BALT_BASE=$B NCS_DATA=$B/ncs-data PY=$B/venv-bd1/bin/python`, `R=$B/b_alt_records`, `W=$B/b_work`, `O=$B/b_alt_out` and `WH=$B/bd1-wheels`:
- `bash scripts/b_alt/run_stage.sh s1a $R $W $O --pyvi-wheel $WH/pyvi-0.1.1-py2.py3-none-any.whl --uts-wheel $WH/underthesea-9.5.0-py3-none-any.whl`. Pin `CENSUS_ALT.json`. If its `floor` is set, stop.
- `… s1b $R $W $O --baselines $B/b_baselines --pyvi-wheel … --uts-wheel … --census-sha <C>`. Pin `PER_IMAGE_ALT.npz` and `S1B.json`.
- `… g0 $R $W $O --npz-sha <N>`. Pin `G0_ALT.json`. On rc 3, stop and write a judge line.
- `… s2 $R $W $O --census-sha <C> --npz-sha <N> --g0-sha <G>`. Pin `RESULT_ALT.json`.

`PER_IMAGE_ALT.npz` and `CENSUS_ALT.json` stay uncommitted. The result note is written by an agent that is neither the coder nor the text writer.

**CPU estimate (PRELIMINARY).** About 3–4 CPU-h. The hard stop is 8 CPU-h, separate from D1's.
