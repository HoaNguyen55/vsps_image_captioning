# Kappa read package, round 2: R2 versus PI agreement on the XM3600-600 overlap (Paper A)

This package is for the one-judge FULL round-2 read that CC-372 (`d8eb3d84`) requires. It answers B1–B6 and N1–N6.

**Expected counts, stated BEFORE the host run (CC-372 B5):**
- self-test: **N = 53** checks, ending `53 checks; selftest ok`;
- mutant harness: **M = 48**, ending `48/48 killed`, with no BAD_TARGET, SURVIVED or CRASH.

The host records are in `scripts/a_cert/host_checks_kappa/` (§7). Nothing has run on the laptop; the laptop only ran `py_compile`, `sha256sum`, `grep`, `sed -n` and `wc`.

## 1. Files (sha256)

| File | sha256 |
|---|---|
| `scripts/a_cert/a_cert_kappa.py` (517 lines, stdlib only) | `1a0be69411da6ca39a939526236ab9f1f108ee1681a380c3541fa958f29c753c` |
| `scripts/a_cert/a_cert_kappa_mutants.py` (159 lines) | `379f2517a725147c6409d506279fa472459b0d9a276fd86cb3f28c063757c0b4` |
| `scripts/a_cert/KAPPA_READ_PACKAGE.md` (this file) | see `SHA256SUMS_KAPPA` |
| round 1 (old side of the `git diff --no-index`) | `a_cert_kappa.py` c964da0c…, `a_cert_kappa_mutants.py` 4e7c6cbf…, package 142f0121…, SUMS ab027ce5… (copies kept outside the repo by the coder; same shas as CC-372 l.4–7) |

**Inputs read** (sha256 on disk):
- plan v1.1 `8ad28f67…`
- analysis reg v1.1 `e564b7b1…`
- CC-367 `f37090f5…`
- CC-372 `d8eb3d8400caf4a5e57986442cf551b737565f4c2e398d4559ac3ba33e229bc7`
- server.py `e3beb936…`
- build_assignment.py `497e5747…`
- assignments `55e07337…` / `fc8aafe9…`
- BUILD_OVERLAP.json `10588e86…`

**Custody of this work.** The coder never opened, listed, stat-ed or hashed `key.json`, any file under `~/vsps_labels*`, or any sealed path. The key structure was taken from build_assignment.py l.115–117, and PI1_SHA from CC-372 l.97–98.

## 2. Closure of CC-372, point by point

All line references are to `a_cert_kappa.py` at `1a0be694`.

### B1. The script reads key.json (ruling 1)

| Ruling | How it is met |
|---|---|
| (a) | New argument `--key` (in `SCORE_ARGS`, l.65–66). Its absolute path joins `_OK` at l.191, only inside the `try` whose `finally` clears `_OK` at l.202; the label files share that try. At every other moment the hook refuses `key.json` (l.77–83). |
| (b) | The key bytes are read once (l.192) and hashed (l.193). They are compared with `P_REAL["key_sha"]` = KEY_SHA `a2cef894…` (l.38; check l.194–195) before any label byte. The same bytes are parsed (l.196). Order: out / argument / pin checks l.174–185, then assignments l.183–188, then key l.191–196, then strata l.197, then label bytes l.199–200. |
| (c) | l.196 reduces the key at once to `{qid: (part, role)}` for the R2 qids. The full dict exists only inside the comprehension. image, class, bucket and named_by are never read into any variable. |
| (d) | `strata` (l.150–169), all label-free. In order: R2 qid in the base with the same screen part (l.156–157); qid in the key (l.158–159); key part = screen part (l.161–162); role in `ROLES[part]` (l.42, l.163–164). `ROLES` is: part 1 {target, ctrl_absent, ctrl_present, foil_absent}; part 2 {target}; part 3 {repeat}. Mapping: target → p1_target; the three control roles → p1_control (pooled; l.165). Counts 457/100/511/42 are checked at l.166–168. |
| (e) | Output = stratum aggregates, two counts and shas. No qid, image, class, bucket, named_by or role is printed or written. The fault print shows type and stage only. Checked by `result_and_stdout_hold_no_qid_or_key_field`: every key text field of the fixture holds "SENTINEL". |
| (f) | Docstring l.1–22, `P_REAL` (no `roles: None`), the mutants and this package hold no "never opens key.json" or "no role source" statement. |

### B2. W11 input design (ruling 2)

| Ruling | How it is met |
|---|---|
| (a) | `--labels-pi1` / `--labels-pi1-sha` must equal PI1_SHA `ba362466…` (l.39, l.181–182), checked before any read. The bytes are checked at l.203–204. The PI's part-1 answers come from L1 only (`src`, l.230). |
| (b) | `--labels-pi2`: L2 must start with the L1 bytes (l.205–206). The PI's part-2 answers are the last line over all of L2 (l.207, l.230). There is no length test. |
| (c) | Part-1 lines after the prefix are ignored (part 1 reads L1 only) and counted at l.221–224 as `pi_part1_lines_after_index = {all_part1, overlap_part1}`. The part comes from the public base `bpart` (l.186, l.222), never from the key. |
| (d) | `pi_part2_overlap_final_after_index` (l.225) counts the distinct overlap part-2 qids that appear after the prefix. Since the last line wins, a qid's winning line lies after the prefix exactly when the qid appears there. |
| (e) | `--labels-r2`: rows must carry "R2"; L1 and L2 rows must carry "PI" (`answers`, l.97–106; calls l.207–208). |
| (f) | Each sha argument must be 64 hex (l.177–178), and the three must be pairwise distinct (l.179–180). Each file's bytes must match its argument (l.203). Every L1/L2 qid must be in the base (l.209–210; L2 holds every L1 line). Every L3 qid must be in the R2 assignment (l.211–212). |
| (g) | Order as in B1(b). |

`SCORE_ARGS` (l.65–66) lists the 10 arguments named in B2; `main` checks `len(argv) == 1 + 2*10` (l.511).

### B3–B6

- **B3.** Completeness faults at l.213–220: "PI part 1 not complete" (L1, all p1 overlap qids = 557), "PI part 2 not complete" (L2, the 511), "R2 not complete" (L3, the 1,068 part-1 and part-2 qids). R2's part 3 is not checked. `rater` no longer has `missing` (l.126–130).
- **B4.**
  - `gate(None)` returns "SENSITIVITY_ONLY" (l.133–136).
  - Every statistic row has `kappa_undefined` (l.141).
  - On a gated row with an undefined kappa, `gate_rule` = `RULE_UNDEFINED` (l.63–64, l.145), whose text cites "CC-372 ruling 3; default pending PI Q1".
  - Raw agreement, PABAK and the table stay beside it. This holds for both gated strata.
- **B5.** The new fixture is in §5 (the judge's suggestion R2 t13 = Y, plus an L2 tail) and the new checks and mutants are in §6. K05/K06 were replaced.
- **B6.** This package, the docstring, and `SHA256SUMS_KAPPA`, which was regenerated last.

### N1–N6

- **N1.** `write_result` (l.243–252) writes into a sibling `mkdtemp` dir and `os.rename`s it to `--out`. On any fault it removes the temp dir. A fault therefore leaves no `--out` and no temp dir (checks `write_fault_leaves_no_temp_dir`, `after_labels_fault_prints_stage_and_writes_nothing`).
- **N2.** `main_maps_score_argv_to_a_label_free_pin_fault` builds a full score argv from the fixture, with the real PI1_SHA. It expects `FAULT Fault label-free` (the pin fault). Mutant S22 unmaps the keys and gets `FAULT KeyError …`.
- **N3.** Carried: reg l.243 (H1–H3 per annotator on the 150 images) needs its own code and read. Not in this file.
- **N4.** The fault line is `FAULT <type> <label-free|after-labels>` (l.261). The stage turns to after-labels at l.199, just before the first label byte. S20 and S21 cover it.
- **N5.**
  - K06 covers U_rate; C04 covers the labels_/practice_ name rule.
  - K08 (control-role pooling) and K09 now die through the count fault, which is a collateral kill. Their named checks are value checks, but the value is never reached.
- **N6.** `scripts/a_cert/__pycache__/` (written by `py_compile`) is never staged.

### Rulings 3–8 as they bind the code

- **Ruling 5.** `n_questions` and `n_both_YN` are both reported.
- **Ruling 6.** The result carries `registered.scope` = "CC-372 ruling 6: …".
- **Ruling 7.** No interval, no `post_hoc` block, no LOG or HEAD checks in the code.
- **Ruling 8.** The pre-checks P1–P8 are operator steps (§8).

## 3. Mapping of each output field to its registered sentence

| Field | Code | Registered text |
|---|---|---|
| last line of a qid wins | `answers` l.97–106 | server.py l.4–6, l.82–86; plan §3 l.30 |
| strata from the screen part plus the key (part, role) | `strata` l.150–169 | plan §2 l.17–19; build_assignment.py l.121–124; CC-372 1(d) |
| `table`, `n_both_YN` | `agree` l.120–123 | plan §4 l.37 ("that both answered Y or N") |
| `kappa`, `raw_agreement`, `pabak` (exact fractions; kappa null when p_e = 1 or n = 0) | `stats` l.109–117 | plan §4 l.37 |
| `kappa_undefined` | l.141 | CC-372 ruling 3 |
| `per_rater` {Y, N, U, A, U_rate, A_rate} | `rater` l.126–130 | plan §4 l.37; CC-372 ruling 4 |
| `gate`, `gate_rule` on p1_target and p2_target only | `gate` l.133–136, `stratum_row` l.139–146, `GATED` l.48 | plan §4 **l.38**; reg l.153; CC-372 ruling 3 |
| no gate on p1_control | `GATED` | plan l.35; reg l.153 |
| `p3_repeat` = `{n_questions}` only | `STAT_STRATA` l.47 | CC-367 1(b) |
| `pi_part1_lines_after_index`, `pi_part2_overlap_final_after_index` | l.221–225 | CC-372 2(c), 2(d) (CC-369 W1/W11) |
| `provenance` (three label shas, key sha, assignment shas, code sha, plan, ruling) | l.233–236 | reg §12 step 5; CC-372 ruling 8 |

**Registered gate.** Plan v1.1 §4 l.38: 0.60, "at or above" = GOLD, on the part-1 target kappa (plan l.37: the 457 part-1 overlap targets, n = those both answered Y or N). The part-2 target kappa gates part 2 the same way. An undefined kappa takes the below-0.60 consequence (CC-372 ruling 3; PI Q1 default).

## 4. Open points left for round 2

1. **K08 and K09 are collateral kills.** Each dies through the count fault before its named value is computed. The named check fails, so the harness rule is met, but the kill comes through the guard, not the value (CC-372 ruling 9 accepted the same for round 1).
2. **"Dropped at once" is a comprehension, not an explicit delete.** The full key dict exists only as a temporary inside the comprehension at l.196.
3. **Host tree name follows the ruling, not the brief.** The tree is `/root/a_kappa_r2` as in CC-372 l.279; the coordinator's message named `/root/a_kappa`. On a failed acceptance there is no rerun without a judge line (CC-372 l.287–288). The coordinator's "fix and re-run in /root/a_kappa2" is not followed, because the ruling binds.

## 5. Hand values in the self-test

**Formula checks** (`stats(YY, YN, NY, NN)`), unchanged from round 1:

| Input | kappa | raw | PABAK |
|---|---|---|---|
| 4,1,1,4 | 3/5 | 4/5 | 3/5 |
| 6,2,0,2 | 6/11 | 4/5 | 3/5 |
| 3,2,0,0 | 0 (defined) | 3/5 | 1/5 |
| 5,0,0,0 | None | 1 | 1 |
| 0,3,0,0 | 0 | 0 | −1 |
| 0,0,0,0 | all None | – | – |

**Gate:** 3/5 → GOLD, 7/10 → GOLD, 6/11 → SENSITIVITY_ONLY, None → SENSITIVITY_ONLY.

**Undefined row:** `stratum_row([(Y,Y)]×3, gated)` gives gate SENSITIVITY_ONLY, kappa None, `kappa_undefined` true, `gate_rule` = RULE_UNDEFINED, raw 1.

**Rater:** `rater([Y,N,U,A])` gives each count 1 and both rates 1/4.

**Fixture world.**
- Images o1 and o2 are overlap; x1 is base only.
- Part-1 targets t01–t13. Controls c1 (ctrl_present), c2 (ctrl_absent), c3 (foil_absent). Part-2 targets s01–s10. Part-3 repeats r1 and r2. Base-only questions z1 (part 1) and z2 (part 2).
- Every key text field holds "SENTINEL".

| Input | Content |
|---|---|
| L1 (PI) | t01–t08 Y; t09 Y then **N**; t10 N; t11 U; t12 N; t13 Y; c1–c3 Y; z1 Y; s01 N, s02 N, s09 N, s10 N; z2 A |
| L2 | L1 + tail: t01 N, c1 N, z1 N (late part-1 lines); s01 N, s01 Y, s02 Y, s03–s05 Y, s06–s08 N; r1 Y, r2 N |
| L3 (R2) | t01–t06 Y; t07 Y then **N**; t08–t10 N; t11 Y; t12 A; **t13 Y**; c1–c3 Y; s01–s04 Y, s05 N, s06 Y, s07–s10 N; r1 N, r2 Y |

**Part-1 targets** (PI from L1, so t01 = Y and the late N is ignored):
- Both Y/N on t01–t10 and t13: table {YY 7, YN 2 (t07, t08), NY 0, NN 2 (t09, t10)}, n_both_YN 11, n_questions 13.
- PI Y 9 / N 2 and R2 Y 7 / N 4 within the table, so p_e = (9·7 + 2·4)/121 = 71/121 and p_o = 9/11.
- **Kappa** = (99/121 − 71/121)/(50/121) = **14/25** = 0.56. **PABAK** = 18/11 − 1 = **7/11** ≈ 0.636, which passes 0.60. **Gate SENSITIVITY_ONLY** (a gate on PABAK would say GOLD), `kappa_undefined` false.
- per_rater over 13 questions: PI {Y 9, N 3, U 1, A 0, U_rate 1/13, A_rate 0}; R2 {Y 8, N 4, U 0, A 1, U_rate 0, A_rate 1/13}.
- Under K01 (first line wins): t07 YY, t09 YN, so YY 8, YN 2, NN 1.
- Under K05 (part 1 from L2): t01 becomes NY, so YY 6, NY 1.

**Other strata:**
- **Part-1 controls:** c1–c3 Y for both (c1's late N ignored). n 3, table YY 3, kappa None, `kappa_undefined` true, raw 1, PABAK 1, no gate key.
- **Part-2 targets** (PI from all of L2): s01 = Y (last of N, N, Y), s02 = Y, s03–s05 Y, s06–s10 N. Table {YY 4, YN 1 (s05), NY 1 (s06), NN 4}, kappa **3/5**, gate **GOLD**.
- **Part 3:** `{"n_questions": 2}`.

**Counts:**
- `pi_part1_lines_after_index` = {all_part1 **3** (t01, c1, z1), overlap_part1 **2** (t01, c1)}.
- `pi_part2_overlap_final_after_index` = **8** (s01–s08; s01 appears twice in the tail, so counting lines would give 9).

**Run checks:**
- The first `run_score` writes only `out/KAPPA_RESULT.json` (p1_target kappa exact "14/25"), leaves no `.tmp_kappa_*`, and puts no SENTINEL, "ctrl_", "foil_" or `"qid` in the body or stdout, and no t01, t13, s01 or z1 in the body.
- The second run prints `FAULT Fault label-free`.
- A wrong R2 sha prints `FAULT Fault after-labels` and leaves no `out` and no temp dir.
- `write_result` onto a non-empty existing dir raises and leaves only that dir.

**Refusals** (each a Fault with its word; the label-free ones use label paths that do not exist, so a refusal placed after the read fails the check):
- out exists; sha argument not 64 hex; shas not distinct; pi1 ≠ PI1_SHA;
- base pin; R2 pin; key sha;
- R2 qid not in the key (t13 removed); key part ≠ screen part (t01 → part 2); part-1 role outside the set (c1 → repeat); part-2 role not target (s01 → ctrl_absent);
- counts (p1_target 457); R2 question not in the base;
- label sha mismatch; L2 not extending L1; PI qid not in the base (zz in the tail); R2 qid outside the R2 assignment (z1); a PI row in the R2 file;
- PI part 1 incomplete (no t13 in L1); PI part 2 incomplete (no s05 in the tail); R2 incomplete (no t13).

**Custody:**
- `refused()` is true for key.json, labels_R2.jsonl, labels_PI.<UTC>.jsonl, practice_R2.jsonl, ~/vsps_labels/… and ~/vsps_labels_b/…, and false for a fixture file.
- The installed hook blocks `open(key.json)`.
- After `score`, `_OK` is empty and `refused(key path)` is true.

**Check count:** 12 unit + 18 world/run + 21 refusals + 2 custody = **53**.

## 6. Mutants (48; each replaces one line; 47 distinct targets, each occurring exactly once by `grep -cF`; K05 and K12 share the `src` line)

| Group | Mutants |
|---|---|
| Statistics and inputs (13) | K01 first line wins; K02 p_e with the Y term only; K03 undefined → 0; K04 PABAK = p_o; K05 PI part 1 from L2; K06 U_rate denominator (N5); K07 part 3 gets statistics; K08 control roles not pooled; K09 parts 2 and 3 swapped; K10 overlap late count = all; K11 W1 counts lines not questions; K12 PI part 2 from L1; K13 late lines not limited to part 1 |
| Gate (7) | G01 `>`; G02 gate on PABAK; G03 threshold 1/2; G04 controls gated; G05 undefined → GOLD; G06 `kappa_undefined` flag dropped; G07 undefined rule text dropped |
| Refusals and fault rule (24) | S01 out exists; S02 64-hex; S03 distinct; S04 PI1_SHA; S05 assignment pins; S06 key sha; S07 qid not in the key; S08 key part; S09 role set; S10 counts; S11 R2 qid not in the base; S12 label shas; S13 L2 prefix; S14 PI qid outside the base; S15 R2 qid outside R2; S16 annotator field; S17 PI part 1 complete; S18 PI part 2 complete; S19 R2 complete; S20 fault prints its message; S21 stage never after-labels; S22 `main` argv keys unmapped (N2); S23 write fault leaves its temp dir (N1); S24 PI/R2 swapped |
| Custody (4) | C01 key.json name not refused; C02 `_OK` not cleared; C03 audit hook never raises; C04 labels_/practice_ name rule off (N5) |

The named checks for each mutant are in `M` of `a_cert_kappa_mutants.py`. Kills that come through another guard are not counted as value kills:
- K08 and K09 die through the count fault.
- K12 dies through a KeyError inside `score`, which `_try` absorbs, so the world checks fail.
- S07, S09, S10, S14, S17 and S18 die because the next guard or step raises something other than the expected Fault, which `_raises` treats as False (accepted in round 1).

## 7. Host recipe and records (h1, CPU only; guards of OPS-1113k/OPS-1113o and CC-372 l.275–288)

- `/root/CPU_WINDOW_OPEN` is checked immediately before the push, the venv step and each launch. If it is absent, nothing is done.
- Every job runs as `env CUDA_VISIBLE_DEVICES= OMP_NUM_THREADS=2 nice -n 19 ionice -c3 taskset -c 16-31`, with `python3 -I -B` from its own venv.
- Tree `/root/a_kappa_r2/scripts/a_cert/` (the two .py files only), scratch `/root/a_kappa_r2_mut`, venv `/root/a_kappa_r2/venv`, records in `/root/a_kappa_r2/out`, tmux session `a_kappa`.
- Nothing else on the host is touched. No data, label, key or assignment file goes to the host: the self-test is synthetic and reads no repo file.
- **Records** (`scripts/a_cert/host_checks_kappa/`, mode a-w): `status.log` (UTC, sha256 of both .py on the host, python version, selftest_rc, mutants_rc), `selftest_kappa.log`, `selftest_kappa.json`, `mutants_kappa.log`, `mutants_result_kappa.json`, `venv_freeze.txt`, `SHA256SUMS`.
- **Folder digest:** `cd <folder>; find . -maxdepth 1 -type f | sort | xargs sha256sum | sha256sum`, taken on both host and laptop. No dotted-IPv4 may appear in the records.
- **Acceptance:** `53 checks; selftest ok`, `48/48 killed`, and status.log shas = §1.

## 8. Real `score` (later; laptop only; CC-372 ruling 8 (a)–(g) and operator pre-checks P1–P8 first)

```bash
python3 -I -B scripts/a_cert/a_cert_kappa.py score \
  --labels-pi1 ~/vsps_labels/xm600_gold/labels_PI.20261112T181546Z.jsonl --labels-pi1-sha ba362466ebd9c50918076dcf5865fbac9c5cd6482288f4251fa1f76e0f2718b4 \
  --labels-pi2 <444 copy of the L-e line> --labels-pi2-sha <its sha from L-e> \
  --labels-r2 <444 copy of the last L-g line> --labels-r2-sha <its sha from L-g> \
  --key ~/vsps_labels/xm600_gold/key.json \
  --assignment manuscript/prereg/2026-11-11_xm600_gold_completion/assignment.json \
  --assignment-r2 manuscript/prereg/2026-11-11_xm600_gold_completion/overlap_r2/assignment.json \
  --out data/results/a_cert_kappa/score
```

`--out` must lie outside `~/vsps_labels*`: the hook refuses writes there.
