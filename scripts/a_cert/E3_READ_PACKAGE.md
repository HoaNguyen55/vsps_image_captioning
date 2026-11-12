# A-CERT E3 read package (E-row code for the top-up labels; for the one-judge code read, addendum §6 step 3)

Spec: `manuscript/prereg/2026-11-11_a_cert/A_CERT_ADDENDUM_E3_v1.md` (`c0eee4fb…`); rulings CC-355 (W1-W5; ruling 2,
O1-O12) and CC-359 (ruling 6). Registered code imported unchanged: `scripts/a_cert/a_cert.py` `2e872588…`.
`a_cert_vp.py`, `build_assignment.py` and `build_topup.py` are not touched. Nothing here is committed or LOGged.
No real-data mode has run anywhere. Written 2026-11-12 (UTC).

## 1. Files (sha256)

| File | sha256 | Status |
|---|---|---|
| `scripts/a_cert/a_cert_e3.py` | `cc56f36fe4764e6c7fd12a45715a72821c82cb7cdd0db6021eb790db23308d6f` | new, to read |
| `scripts/a_cert/a_cert_e3_mutants.py` | `ef933c83c607dff4efc700b1a08545ea23df2c3ab3e34a92bc1bcf5eb4ef2e2d` | new, to read |
| `scripts/a_cert/host_checks_e3code/*` | see `SHA256SUMS_E3CODE` | host records |
| `scripts/a_cert/a_cert.py` | `2e872588baf6109fad20111aecd25e2504fd0096f9033a95649027a2eed46cf4` | committed, imported, unchanged |

Host checks on hc2, CPU only, in the code-only tree `/root/a_e3code_tree`, run 2026-11-12 from 15:01:56Z to 15:02:28Z:

| Check | Result | Record |
|---|---|---|
| Self-test | 59/59, `selftest ok` | `selftest_e3.json`; `script_sha256` = cc56f36f…, `a_cert_sha256` = 2e872588… |
| Mutants | 56/56 KILLED | `mutants_result_e3.json`; `source_sha256` = cc56f36f… |

A mutant counts as KILLED only under three conditions:
- the run exits non-zero;
- one of the checks named for that mutant in `M` fails;
- no `no_exception` entry is present. A crash is never counted as a kill.

`status.log` gives the sha256 of every file in the host tree, plus the start and end UTC.

## 2. What maps to which addendum line

| Addendum | Code (`a_cert_e3.py`) |
|---|---|
| §0 S_E (7a ∪ 7c passing models, two prompts each) | `load_extras` (the checks of build_topup step 3; both prompts required); `check_build` (CC-359 LC4': `new_systems` and every `--extra` sha in `BUILD_TOPUP1.json`); `S_E_REAL` (real mode) |
| §0 label of every row | `ROW_LABEL`, printed on FREEZE_E3 and on the result. The selftest checks it verbatim against the addendum. |
| §2 disclosures | `DISCLOSE`. The selftest checks them verbatim. |
| CC-359 1(b): the added-model line | `D7C` on every row of a 7c system (`tag`). The selftest checks it verbatim against CC-359 (whitespace normalised). |
| §3 "a_cert freeze logic on 12 + S_E" | `e_world` (the twelve from `a_cert._load_world()` unchanged, plus S_E) and `freeze_e3_core` |
| §3 C-ref certificates, pairs with ≥ 1 S_E member | `e_pairs`. Per pair: the C-ref grid, `w*`, V-H, the first-two row, `dabs` and the lengths (as FREEZE). |
| §3 C-label verdicts of the same pairs (W1) | `clabel` and `clabel_cells` |
| §3 budgets β(N_s; w) and §4.4 low ends | `budgets`, per S_E system on I600 |
| §3 "the 12-system gate must reproduce before FREEZE_E3" | `e3_freeze`, real mode: `a_cert.gate_core` in memory must be all ok. It also checks that the 12-system FREEZE sha begins `c51ea7dc`. |
| §4 completed status | `score_e3_core`: `human(base)` ∪ `human(top-up)` via `a_cert.human`, which uses part-1 targets only, takes the last line and never overrides Open Images; `a_cert.counts` |
| §4 Q7: agreement-only answers | old_repeat, controls and part 3 never enter `h`, through `a_cert.human`'s role and part filter. Mutant E1_06 checks this. |
| §5 E1 (O1, O11) | `fam_slopes` on an s75-shaped context per model (`e_ctx`), using the Q25 `idx_boot[:500]` |
| §5 E2 (O2, O3, W5) | `e2_rows`: within (the two prompts of a model) and cross, each printed apart; w0 primary, the grid secondary |
| §5 E3 | budget coverage with the FREEZE_E3 ⌊β(w0)⌋ |
| §5 E4 (O6) | `a_cert.h3_row` on `n_u` (N_u'), with no verdict word |
| §5 E5 (O4, W5) | detailed − short: 100·F_c (reg, lo, hi), P_c, ln M. Points only. |
| §5 E6 (O5, W5) | old_repeat against the base last line; controls by role and by hint coverage; top-up part-3 repeats; old_repeat ∩ base part 3 |
| §5 last line: top-up labels never enter the twelve systems' rows | A Fault if a top-up target is a base target or is named by one of the twelve |
| §6 step 1 (part-1 score first) and step 3 refusals | `e3_score` refuses in each of these cases: no FREEZE_E3 pin line; no part-1 result pin line; no top-up session-end line; the result already exists |
| A-CERT §12 step 5 fault rule | Every statistic is computed in memory, then one atomic write. On any fault it prints `FAULT <type>` only and writes nothing. |

## 3. Readings I had to choose (each a judge item)

- **R1. Where the extra-caption hook lives.** Addendum §3 says it goes "in `a_cert.py` only". The brief forbids changing `a_cert.py`, so the hook is `e_world` in the new file.
  - `_load_world()` / `_score_world()` are called unchanged, and the S_E sets are then added to `sys`, `ms_all` and `ms`.
  - That matches "after its unchanged call of `load_systems()`" in substance, but not in file.
  - `e3-freeze` runs the 12-system gate in memory (`a_cert.gate_core`, the same function `a_cert.py gate` uses). It does not rewrite `gate.json`.
- **R2. S_E.** In real mode, S_E must equal the eight names the brief gives (CC-359 ruling 6). It must also equal `BUILD_TOPUP1.json` `counts.new_systems`, with the file shas equal to its `--extra` shas.
  - The 7c disclosure follows the path segment `/ATTR_H1_7c/`, as the pull layout of CC-359 4(c) sets it.
- **R3. Pairs.**
  - 12 × 8 + C(8,2) = 124 pairs: 4 within, 120 cross.
  - System order: `BUILD.json` order, then S_E sorted.
  - Image set (O3): I537 if either member is a Q3 system, I600 otherwise.
  - The cross row is one row; it is not split by partner family.
- **R4. What FREEZE_E3 holds beyond §3.**
  - The same per-pair fields as FREEZE.
  - The counts certified per w.
  - The E4 evaluability (φ1, φ2 on N_u' are label-free) and the E3 budget declarations, all as label-free declarations.
  - Nulls and the H2a evaluability declaration are not included, because E2 carries no verdict.
  - The FREEZE §V.4a fault ("a C-ref certificate at w = 0") is **not** inherited. It binds H2d. Under the reference gold a C-ref certificate at w = 0 cannot occur anyway: no mention is known absent.
- **R5. E1.**
  - P_c in percent, from `bracket`'s registered `oi_draws_extended` on an s75-shaped context built by `e_ctx`: caption_rows, per-image recall and M = mentions per caption, as `s75_context` l.165-170.
  - The bootstrap is the Q25 `idx_boot[:500]` (O1).
  - The interval is v3's 2.5/97.5 `nanpercentile`.
  - In real mode, `e_ctx` must reproduce `s75_context` for the six Q25 systems (a and pr exactly, M within 1e-12), or the freeze faults.
- **R6. E2.**
  - No verdict words: `h2a_rule`'s label, limit and refuted fields are dropped.
  - Counts at w0 and over the grid.
  - The interval as A-CERT H2a: `boot_weights(600, default_rng(20261111), 2000)`, with the certified set fixed. The stream sha is printed.
  - Truth is the completed P_c in the FREEZE_E3 direction, at reg and at both ends (`a_cert.confirmed`).
  - A twelve-system member's P_c uses base labels only. That is equal to the merged map, because the guard of §2 holds.
- **R7. E3.**
  - covered = x_hi ≤ ⌊β(N_s; w0)⌋, with β taken from FREEZE_E3.
  - x and x_hi are computed as A-CERT H2b.
  - covered at each grid w > 0 is printed as secondary.
  - There is no 11-of-12 rule, only the count.
- **R8. E4.**
  - H3 through `a_cert.h3_row` on N_u'.
  - Bootstrap B = 2000, seed 20261111; the stream sha is printed.
  - `reading_no_verdict` is removed. Only "NOT EVALUABLE" can be printed (O6).
  - `n_ref_named_completed_absent` is printed beside it, as H3 does.
  - There is no Bonferroni column.
- **R9. E5.**
  - detailed − short of 100·F_c, with R = `R_pos`, the registered gold (i) recall of the s75 path. Given at reg, lo and hi.
  - ΔP_c and Δln M at reg.
  - Points only; the E5 row carries the 7c line if the model is from 7c.
- **R10. E6.**
  - old_repeat: compared with the last line of the pair's base part-1 qid (CC-355 ruling 2, O5), over items with Y/N in both. The top-up U, A and unanswered counts and the base U and A counts are printed apart.
  - Controls: `ctl_row` per role, and the absent controls by hint coverage (plan §4, as A-CERT S1).
  - Part-3 agreement: A-CERT's own definition, i.e. equal answers among the answered part-3 items.
  - Also printed: the count of old_repeat items that are also base part-3 pairs.
- **R11. `e3-score` inputs and the meaning of the LOG lines.** The brief's `--labels/--labels-sha/--key` is extended by `--topup-labels/--topup-labels-sha/--topup-key`, because §4 needs both sessions.
  - The base copy must be the copy the part-1 score read: its sha must equal `A_CERT_RESULT.json` `provenance.labels_sha256`. The base key must equal that provenance and `a2cef894`.
  - The required LOG lines are each a line containing:
    - `FREEZE_E3` and the FREEZE_E3 sha;
    - `A_CERT_RESULT` and the sha of the part-1 result;
    - `topup1` and the top-up copy sha (the session-end line);
    - `topup1` and the top-up `key.json` sha (the LC5 PIN line).
  - Base part 1 must be complete (2,233). Top-up completeness is not required: unanswered pairs go to the remainder (§4).
- **R12. Guards I added (code-fault guards, like the §5 STOP).** Each of these is a Fault:
  - a top-up target that is a base target;
  - a top-up target named by one of the twelve;
  - an old_repeat that is not a base part-1 target;
  - an image-set size that differs from FREEZE_E3.
  
  On real data any of them falls under the fault rule.
- **R13. Custody.**
  - The hook refuses, in every mode except for e3-score's four named inputs:
    - `vsps_labels/`;
    - the sealed paths of `a_cert.DENY`;
    - any `labels_*.jsonl`, `practice_*.jsonl` or `key.json`.
  - It also refuses any `assignment.json` except the base public copy, which the in-memory gate reads as `a_cert gate` does.
  - Label-free modes also refuse such a path given as an argument.
  - Outputs carry counts, labels and sha only. A sentinel caption word is checked absent from every output and from stdout.
- **R14. Kappa and W3.** No kappa is computed. O7 needs the second annotator, and N5 needs the base kappa outcome; both are a text field (`kappa`). The W3 disclosure (the PI saw the part-1 result before the top-up ended) cannot be known by code. The result reader adds it.
- **R15. Output paths.** `data/results/a_cert_e3/freeze/FREEZE_E3.json` and `data/results/a_cert_e3/score/A_CERT_E3_RESULT.json`. Whether they are git-ignored is "chưa kiểm".
- **R16. Host tree.** It holds code only, with these extra files beyond the import closure:
  - the addendum and `CC-359.txt`, for the verbatim checks;
  - `scripts/person_uncap.py`;
  - `data/coco_probe/{coco80_vi.json, chair_synonyms.txt}`. These are lexicon resources read at import by the reused modules, and are the same two files as in `/root/a_cert_tree`.
  
  The tree has no caption, label, key, assignment or Open Images file.

## 4. Run recipe

| Mode | Where | Why |
|---|---|---|
| `selftest` and the mutant harness | rented host (CPU, niced) or any host | synthetic only |
| `e3-freeze` | **laptop only, named exception** | It reads the Open Images labels, the references and the S_E captions (pull copies). These never go to a rented host (run doc §7, §9.1; CC-355 N-1 analogue). |
| `e3-score` | **laptop only, named exception** | It also reads the PI's base and top-up label copies and both key files. |

Order on the laptop, each step with one OPS line:
1. One-judge code read; gatekeeper commit of the files in `SHA256SUMS_E3CODE`.
2. After the top-up build (the LC4' checks), run `e3-freeze`.
3. Hash FREEZE_E3, make a 444 copy, gatekeeper commit, then the pin line `… FREEZE_E3 … <sha>`.
4. Part-1 score. Then a pin line containing `A_CERT_RESULT` and the result sha.
5. Top-up session end. The LC7 line must contain `topup1` and the copy's sha. The LC5 PIN line already names the top-up `key.json` sha.
6. `e3-score` once. Log the start and end UTC, the exit status and the shas only. A `FAULT <type>` follows A-CERT §12 step 5.

```
cd /mnt/d/vsps_image_captioning
P=.session_backup/machines/ATTR_H1/root/a_e3/out; Q=.session_backup/machines/ATTR_H1_7c/root/a_e3/out
OMP_NUM_THREADS=2 nice -n 15 ~/.venvs/c_stage1_lists/bin/python -I -B scripts/a_cert/a_cert_e3.py e3-freeze --extra \
  $(for d in $P:$P/passed_7a.txt $Q:$Q/passed_7c.txt; do for k in $(cat ${d#*:}); do for m in short detailed; do \
    echo ${d%%:*}/ae3_${k}_xm600-$m.preds.json; done; done; done)

OMP_NUM_THREADS=2 nice -n 15 ~/.venvs/c_stage1_lists/bin/python -I -B scripts/a_cert/a_cert_e3.py e3-score \
  --labels ~/vsps_labels/xm600_gold/labels_PI.<UTC_part1>.jsonl --labels-sha <sha the part-1 score read> \
  --key ~/vsps_labels/xm600_gold/key.json \
  --topup-labels ~/vsps_labels/xm600_gold_topup1/labels_PI.<UTC_topup>.jsonl --topup-labels-sha <session-end sha> \
  --topup-key ~/vsps_labels/xm600_gold_topup1/key.json
```

Host commands for any later re-check (code-only tree; never a data file):
```
ssh -o BatchMode=yes hc2 'cd /root/a_e3code_tree && O=/root/outputs_e3code_checks; \
  env CUDA_VISIBLE_DEVICES= OMP_NUM_THREADS=2 nice -n 19 ionice -c3 /root/vsps/.venv/bin/python -I -B scripts/a_cert/a_cert_e3.py selftest --out $O/selftest_e3.json > $O/selftest_e3.log 2>&1; \
  env CUDA_VISIBLE_DEVICES= OMP_NUM_THREADS=2 nice -n 19 ionice -c3 /root/vsps/.venv/bin/python -I -B scripts/a_cert/a_cert_e3_mutants.py $O/mut > $O/mutants_e3.log 2>&1'
```

## 5. Hand values in the self-test (mini world)

The mini world has two images, i and j.

| Item | i | j |
|---|---|---|
| Open Images | a present, b absent | c present, e absent |
| References | {a,c}, {c,u} | {d}, {c} |
| q (Q25) | {a} | {c} |
| r (Q3, scored on j only) | {a,b} | {d} |
| S (`ae3_aa_xm600-short`) | {a,c,d} | {c,e,u} |
| D (`ae3_aa_xm600-detailed`) | {a,b,c,d,e} | {c,d,e,u} |

Labels:
- Base targets: (i,c) gets N then Y, so the last line is Y; (j,d) is N.
- Top-up targets: (i,d) Y and (i,e) U.
- The old_repeat items are (i,c) Y and (j,d) U.

Freeze values checked by hand:
- **Pairs:** (q,D), (q,S), (r,D), (r,S), (D,S). Image counts 2, 2, 1, 1, 2; only (D,S) is within.
- **C-ref at w0:** all NOT CERTIFIED. Δ_min is 0, 0, 0, 0 and −3/20.
- **w\*:** for (q,D) it lies in (0.9, 0.95), where β(f1 = 1, w) < 4 holds just above it and fails just below. The other four are NI.
- **C-label:**

  | Pair | Verdict | Δ_min |
  |---|---|---|
  | (q,D) | CERTIFIED | 1/4 |
  | (q,S) | CERTIFIED | 1/5 |
  | (r,D) | NOT CERTIFIED | −1/3 |
  | (r,S) | NOT CERTIFIED | −1/2 |
  | (D,S) | NOT CERTIFIED | −1/10 |

- **Budgets:**

  | System | n | t | U | f1 | φ1 | φ2 | L̂ | low | ⌊β(w0)⌋ |
  |---|---|---|---|---|---|---|---|---|---|
  | D | 8 | 4 | 4 | 3 | 3 | 1 | 2.25 | 0.78125 | 37 |
  | S | 5 | 3 | 2 | 2 | 2 | 1 | 1 | 0.8 | – |

- **E4 declaration:** N_u' = 4, φ1 = φ2 = 1, f̂0 = 0.25, NOT EVALUABLE.

E rows checked by hand:
- **E1:** P_c(D) = 4/7 (lo 1/2, hi 5/8); P_c(S) = 4/5.
- **E5:** ΔF = 100(8/11 − 8/9), ΔP = 100(4/7 − 4/5), Δln M = ln 1.5.
- **E2:** cross confirmed (T, T, F, F), so V_n = 0.5; within V_n = 1.
- **E3:** x/x_hi are D 1/2 and S 1/1.
- **E4:** X = 1, X_hi = 2, D = 0.75, D_hi = 1.75.
- **E6:** old_repeat agreement 1/1 (one U), controls 1/1, part 3 1/1, old ∩ base part 3 = 1.

The 40-image A-CERT fixture with two models (one under `ATTR_H1_7c/`) exercises:
- the modes end to end;
- every refusal;
- the fault rule;
- the once-only writes;
- the 54-pair count;
- the O3 image sets;
- E1 = 100·`pc_ends` P_c;
- the O1 interval against a recomputation;
- `e_ctx` against the fixture's `s75` context.

## 6. Host command log (hc2; for the coordinator's OPS line; UTC from `date -u` on the host)

| UTC | Command (summary) |
|---|---|
| 11:50:04Z | `date`; a read-only file listing of `/root/a_cert_tree` (twice, the second without `manuscript/`); `ls` of the venv python; `nproc`; `uptime` |
| 11:53:28Z | `mkdir /root/a_e3code_tree /root/outputs_e3code_checks`; `tar x` of 37 code files from the laptop (git-clean); `sha256sum a_cert.py` = 2e872588 |
| 13:59:36Z | push `a_cert_e3.py`, `a_cert_e3_mutants.py`, `CC-359.txt`; self-test try: `ModuleNotFoundError person_uncap` |
| 13:59:56Z | push `scripts/person_uncap.py`; self-test import probe |
| 14:00:07Z | self-test try: `FileNotFoundError` on `data/coco_probe/coco80_vi.json` |
| 14:00:16Z | push the two `data/coco_probe` lexicon files; self-test try 57/57 ok |
| 14:00:24–14:00:54Z | trial mutant run, 52/55. F03 and F12 crashed and E1_03 survived; the check code was fixed. |
| ~14:01Z | system `python3 -c` reading two mutant JSON records (failed-check names) |
| 14:11:33–14:12:04Z | record run 1: self-test 58/58, mutants 54/55 (F12 crash). Fixed, and the records were deleted. |
| ~14:13Z | system `python3 -c` reading one mutant JSON record |
| 14:23:46Z | push the fixed code; `rm -rf /root/outputs_e3code_checks/*`; record run 2: self-test 58/58, mutants 55/55. Superseded by run 3. |
| ~14:24Z | `tar c` of the five records, pulled to `scripts/a_cert/host_checks_e3code/` |
| 14:24:39Z | `stat -c %Z` of four tree files; `tmux ls` (names only) |
| 15:01:56Z | push the code with `row_label` on every E row (one check and one mutant added); `rm -rf /root/outputs_e3code_checks/*`; **record run 3 (the record)**: start 15:01:56Z, self-test rc 0 at 15:01:57Z, mutants rc 0 at 15:02:28Z, DONE 15:02:28Z |
| 15:22:23Z | `tar c` of the five run-3 records, pulled to `scripts/a_cert/host_checks_e3code/`, replacing the run-2 copies. Last ssh to hc2. |

Every run of the venv python had `CUDA_VISIBLE_DEVICES=` set, with `nice -n 19 ionice -c3` and `OMP_NUM_THREADS=2`. No GPU process was started.

Nothing under `/root/a_e3`, `/dev/shm/a_e3`, `/root/outputs`, `/root/vsps` (its venv python only executed), `/root/c_attr_score`, `/root/a_vp_tree` or `/root/ncs-data` was touched. Every ssh output was filtered for IP-like strings.

**Deviations from the brief (for an OPS DEVIATION line):**
- Two read-only inspections of mutant JSON records ran under the host's system `python3 -c`, at about 14:01Z and 14:13Z. They ran without `CUDA_VISIBLE_DEVICES=`, nice or ionice. They imported only `json` and read files in `/root/outputs_e3code_checks/`.
- The record pulls were raw `tar c | tar x` streams from host to laptop, so their bytes could not pass through the IP filter. The records were grepped afterwards and hold only check names, counts and shas.

**What the host records do not cover.** No synthetic test executes:
- the `P is P_REAL` branches of `e3_freeze` and `e3_score` (HEAD-blob and sha checks, the 12-FREEZE prefix, the in-memory 12-system gate, `S_E_REAL`, `KEY_SHA`);
- `real_world`;
- `main`'s `e3-score` argument parsing;
- `ctx_check` against the real `bracket.s75_context`.

Their first execution is the laptop `e3-freeze`. A failure there prints `FAULT <type>` and writes nothing, and it is reversible because the freeze is label-free.

A grep of the reused modules found no read of a basename the stricter guard refuses: `build_assignment.py` names `key.json` / `assignment.json` only in `build()`, which the freeze never calls. The G2-B prereg JSON names none.

## 7. Open questions for the judge

1. Is R1 acceptable: the hook in the new file, which leaves `a_cert.py` byte-identical, against the addendum's "in `a_cert.py` only"? Or does this need a ruling line?
2. The LOG-line conventions of R11, and the base copy = the part-1 scored copy.
3. Should the E2 cross row be split by partner family (Q25 / Q3 / other S_E)?
4. The added guards of R12: they turn an impossible-by-construction state into a fault under the single-run rule. Keep them?
5. Are e3-freeze and e3-score accepted as laptop-only named exceptions (one OPS DEVIATION line each, as CC-355 N-1)?
6. W3 and N5 are text that the result reader adds. Confirm.
7. Top-up completeness. `e3-score` accepts any LOG line holding `topup1` and the copy's sha. LC7 writes a session-end line for every session, so a copy from an intermediate session would pass and spend the single run. The two options:
   - (a) refuse unless every top-up part-1 qid in the key is answered, as `a_cert` does for base part 1;
   - (b) as coded now, relying on the operator to pass the final copy.

   I recommend (a). The code is unchanged pending the ruling.
8. Every E row carries `row_label` = the §0 label, besides the result-level `label` (check `row_label_on_every_E_row`). E4's own `label` key holds only "NOT EVALUABLE" or null (O6).
